from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.receipt import ImportReceipt, ImportReceiptDetail
from app.models.inventory import Inventory
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.schemas.receipt import ImportReceiptCreate, ImportReceiptResponse
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/imports", tags=["Import Receipts Management"])

def _format_import_response(receipt: ImportReceipt) -> dict:
    total_amount = sum(d.quantity * d.unit_price for d in receipt.details)
    details_formatted = []
    for d in receipt.details:
        stock_qty = d.product.inventory.quantity if d.product.inventory else 0
        prod_dict = {
            "id": d.product.id,
            "code": d.product.code,
            "name": d.product.name,
            "category_id": d.product.category_id,
            "unit_id": d.product.unit_id,
            "minimum_stock": d.product.minimum_stock,
            "description": d.product.description,
            "is_active": d.product.is_active,
            "created_at": d.product.created_at,
            "updated_at": d.product.updated_at,
            "category": d.product.category,
            "unit": d.product.unit,
            "current_stock": stock_qty
        }
        details_formatted.append({
            "id": d.id,
            "product_id": d.product_id,
            "quantity": d.quantity,
            "unit_price": d.unit_price,
            "total_price": d.quantity * d.unit_price,
            "product": prod_dict
        })

    return {
        "id": receipt.id,
        "receipt_code": receipt.receipt_code,
        "supplier_id": receipt.supplier_id,
        "created_by": receipt.created_by,
        "receipt_date": receipt.receipt_date,
        "note": receipt.note,
        "status": receipt.status,
        "supplier": receipt.supplier,
        "creator": receipt.creator,
        "details": details_formatted,
        "total_amount": total_amount
    }

@router.get("", response_model=List[ImportReceiptResponse])
def get_import_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    receipts = db.query(ImportReceipt).order_by(ImportReceipt.id.desc()).all()
    return [_format_import_response(r) for r in receipts]

@router.get("/{receipt_id}", response_model=ImportReceiptResponse)
def get_import_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    receipt = db.query(ImportReceipt).filter(ImportReceipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu nhập kho")
    return _format_import_response(receipt)

@router.post("", response_model=ImportReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_import_receipt(
    receipt_in: ImportReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE"]))
):
    # Generate receipt code (e.g. PN202609141025)
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y%m%d%H%M%S%f")
    receipt_code = f"PN{date_str}"

    try:
        # 1. Create Header
        receipt = ImportReceipt(
            receipt_code=receipt_code,
            supplier_id=receipt_in.supplier_id,
            created_by=current_user.id,
            receipt_date=receipt_in.receipt_date or now,
            note=receipt_in.note,
            status="COMPLETED"
        )
        db.add(receipt)
        db.flush()

        # 2. Process Details & Atomic Stock Increase
        for item in receipt_in.details:
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Số lượng nhập phải lớn hơn 0")
            
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Sản phẩm ID {item.product_id} không tồn tại")

            # Add detail line
            detail = ImportReceiptDetail(
                receipt_id=receipt.id,
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price
            )
            db.add(detail)

            # Update inventory (+ qty)
            inv_query = db.query(Inventory).filter(Inventory.product_id == item.product_id)
            bind = db.get_bind()
            if bind and bind.dialect.name != "sqlite":
                inv_query = inv_query.with_for_update()
            inventory = inv_query.first()
            if not inventory:
                inventory = Inventory(product_id=item.product_id, quantity=0)
                db.add(inventory)
                db.flush()

            inventory.quantity += item.quantity
            inventory.updated_at = now

            # Log stock movement
            movement = StockMovement(
                product_id=item.product_id,
                movement_type="IMPORT",
                reference_type="IMPORT_RECEIPT",
                reference_id=receipt.id,
                quantity=item.quantity,
                created_by=current_user.id,
                created_at=receipt.receipt_date
            )
            db.add(movement)

        # Commit Transaction
        db.commit()
        db.refresh(receipt)
        return _format_import_response(receipt)

    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Lỗi khi thực hiện transaction nhập kho: {str(e)}")
