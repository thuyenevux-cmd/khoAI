from typing import List, Optional
from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from app.models.receipt import ExportReceiptDetail, ExportReceipt
from app.schemas.inventory import InventoryResponse, LowStockAlertResponse
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/inventory", tags=["Inventory Engine & Alerts"])

def _determine_stock_status(current_stock: int, min_stock: int) -> str:
    if current_stock == 0:
        return "OUT_OF_STOCK"
    elif current_stock <= min_stock:
        return "LOW_STOCK"
    return "NORMAL"

@router.get("", response_model=List[InventoryResponse])
def get_inventories(
    category_id: Optional[int] = None,
    stock_status: Optional[str] = None, # NORMAL, LOW_STOCK, OUT_OF_STOCK
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    query = db.query(Inventory).join(Product).filter(Product.is_active == True)
    if category_id:
        query = query.filter(Product.category_id == category_id)
        
    inventories = query.all()
    results = []

    for inv in inventories:
        p = inv.product
        status_val = _determine_stock_status(inv.quantity, p.minimum_stock)
        if stock_status and status_val != stock_status:
            continue
            
        stock_qty = inv.quantity
        prod_dict = {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "category_id": p.category_id,
            "unit_id": p.unit_id,
            "minimum_stock": p.minimum_stock,
            "description": p.description,
            "is_active": p.is_active,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "category": p.category,
            "unit": p.unit,
            "current_stock": stock_qty
        }
        
        results.append({
            "id": inv.id,
            "product_id": inv.product_id,
            "quantity": inv.quantity,
            "updated_at": inv.updated_at,
            "product": prod_dict,
            "status": status_val
        })

    return results

@router.get("/alerts", response_model=List[LowStockAlertResponse])
def get_low_stock_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    # Query products where current_stock <= minimum_stock
    products = db.query(Product).join(Inventory).filter(
        Product.is_active == True,
        Inventory.quantity <= Product.minimum_stock
    ).all()

    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)

    alerts = []
    for p in products:
        stock_qty = p.inventory.quantity if p.inventory else 0
        
        # Calculate export in last 30 days
        export_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= thirty_days_ago
        ).scalar() or 0

        status_val = "OUT_OF_STOCK" if stock_qty == 0 else "BELOW_MINIMUM"

        alerts.append({
            "product_id": p.id,
            "product_code": p.code,
            "product_name": p.name,
            "current_stock": stock_qty,
            "minimum_stock": p.minimum_stock,
            "export_30_days": int(export_30),
            "status": status_val
        })

    return alerts
