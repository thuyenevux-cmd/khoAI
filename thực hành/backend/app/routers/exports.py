from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.receipt import ExportReceipt, ExportReceiptDetail
from app.models.inventory import Inventory
from app.models.stock_movement import StockMovement
from app.models.product import Product
from app.schemas.receipt import ExportReceiptCreate, ExportReceiptResponse
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/exports", tags=["Export Receipts Management"])

def _format_export_response(receipt: ExportReceipt) -> dict:
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
            "product": prod_dict
        })

    return {
        "id": receipt.id,
        "receipt_code": receipt.receipt_code,
        "created_by": receipt.created_by,
        "receipt_date": receipt.receipt_date,
        "receiver": receipt.receiver,
        "note": receipt.note,
        "status": receipt.status,
        "creator": receipt.creator,
        "details": details_formatted
    }

@router.get("", response_model=List[ExportReceiptResponse])
def get_export_receipts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    receipts = db.query(ExportReceipt).order_by(ExportReceipt.id.desc()).all()
    return [_format_export_response(r) for r in receipts]

@router.get("/{receipt_id}", response_model=ExportReceiptResponse)
def get_export_receipt(
    receipt_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    receipt = db.query(ExportReceipt).filter(ExportReceipt.id == receipt_id).first()
    if not receipt:
        raise HTTPException(status_code=404, detail="Không tìm thấy phiếu xuất kho")
    return _format_export_response(receipt)

@router.post("", response_model=ExportReceiptResponse, status_code=status.HTTP_201_CREATED)
def create_export_receipt(
    receipt_in: ExportReceiptCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE"]))
):
    now = datetime.now(timezone.utc)
    date_str = now.strftime("%Y%m%d%H%M%S%f")
    receipt_code = f"PX{date_str}"

    try:
        # 1. Create Header
        receipt = ExportReceipt(
            receipt_code=receipt_code,
            created_by=current_user.id,
            receipt_date=receipt_in.receipt_date or now,
            receiver=receipt_in.receiver,
            note=receipt_in.note,
            status="COMPLETED"
        )
        db.add(receipt)
        db.flush()

        # 2. Process Details & Anti-Negative Stock Validation
        for item in receipt_in.details:
            if item.quantity <= 0:
                raise HTTPException(status_code=400, detail="Số lượng xuất phải lớn hơn 0")
            
            product = db.query(Product).filter(Product.id == item.product_id).first()
            if not product:
                raise HTTPException(status_code=404, detail=f"Sản phẩm ID {item.product_id} không tồn tại")

            # Lock inventory row (Pessimistic Locking for MySQL/Postgres)
            inv_query = db.query(Inventory).filter(Inventory.product_id == item.product_id)
            bind = db.get_bind()
            if bind and bind.dialect.name != "sqlite":
                inv_query = inv_query.with_for_update()
            inventory = inv_query.first()
            current_stock = inventory.quantity if inventory else 0

            # STRICT ANTI-NEGATIVE STOCK GUARD
            if current_stock < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Số lượng tồn kho sản phẩm '{product.name}' (Mã: {product.code}) không đủ để xuất! (Tồn hiện tại: {current_stock}, Yêu cầu xuất: {item.quantity})"
                )

            # Deduct stock
            inventory.quantity -= item.quantity
            inventory.updated_at = now

            # Insert detail
            detail = ExportReceiptDetail(
                receipt_id=receipt.id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.add(detail)

            # Log stock movement
            movement = StockMovement(
                product_id=item.product_id,
                movement_type="EXPORT",
                reference_type="EXPORT_RECEIPT",
                reference_id=receipt.id,
                quantity=item.quantity,
                created_by=current_user.id,
                created_at=receipt.receipt_date
            )
            db.add(movement)

        # Commit Transaction
        db.commit()
        db.refresh(receipt)
        return _format_export_response(receipt)

    except HTTPException as he:
        db.rollback()
        raise he
    except Exception as e:
        db.rollback()
        print(f"DEBUG EXPORT ERROR: {type(e)} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi thực hiện transaction xuất kho: {str(e)}")
