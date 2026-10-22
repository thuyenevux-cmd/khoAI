from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.product import Product
from app.models.supplier import Supplier
from app.models.receipt import ImportReceipt, ExportReceipt, ImportReceiptDetail, ExportReceiptDetail
from app.models.inventory import Inventory
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/dashboard", tags=["Dashboard Metrics & Charts"])

@router.get("")
def get_dashboard_metrics(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    # KPI Counters
    total_products = db.query(Product).filter(Product.is_active == True).count()
    total_suppliers = db.query(Supplier).filter(Supplier.status == "ACTIVE").count()
    total_imports = db.query(ImportReceipt).count()
    total_exports = db.query(ExportReceipt).count()

    # Low stock items count
    low_stock_count = db.query(Product).join(Inventory).filter(
        Product.is_active == True,
        Inventory.quantity <= Product.minimum_stock
    ).count()

    total_inventory_quantity = db.query(func.sum(Inventory.quantity)).scalar() or 0

    # Calculate estimated total inventory valuation
    products = db.query(Product).filter(Product.is_active == True).all()
    estimated_inventory_value = 0
    for p in products:
        stock = p.inventory.quantity if p.inventory else 0
        latest_detail = db.query(ImportReceiptDetail).filter(
            ImportReceiptDetail.product_id == p.id
        ).order_by(ImportReceiptDetail.id.desc()).first()
        price = latest_detail.unit_price if latest_detail else 0.0
        estimated_inventory_value += int(stock * price)

    # Top 5 exported items (Last 30 days)
    now = datetime.now(timezone.utc)
    thirty_days_ago = now - timedelta(days=30)
    top_exports_query = db.query(
        Product.code,
        Product.name,
        func.sum(ExportReceiptDetail.quantity).label("total_export")
    ).join(ExportReceiptDetail, Product.id == ExportReceiptDetail.product_id)\
     .join(ExportReceipt, ExportReceiptDetail.receipt_id == ExportReceipt.id)\
     .filter(ExportReceipt.receipt_date >= thirty_days_ago)\
     .group_by(Product.id)\
     .order_by(func.sum(ExportReceiptDetail.quantity).desc())\
     .limit(5).all()

    top_exported_items = [
        {"code": row.code, "name": row.name, "quantity": int(row.total_export)}
        for row in top_exports_query
    ]

    # Low stock warnings list (Top 5)
    low_stock_items = db.query(Product).join(Inventory).filter(
        Product.is_active == True,
        Inventory.quantity <= Product.minimum_stock
    ).limit(5).all()

    low_stock_warnings = [
        {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "current_stock": p.inventory.quantity if p.inventory else 0,
            "minimum_stock": p.minimum_stock
        }
        for p in low_stock_items
    ]

    # Mock chart series monthly stats (Current year months or recent 6 months)
    monthly_chart = [
        {"month": "T4/2026", "nhap": 120, "xuat": 90},
        {"month": "T5/2026", "nhap": 200, "xuat": 150},
        {"month": "T6/2026", "nhap": 180, "xuat": 210},
        {"month": "T7/2026", "nhap": 250, "xuat": 190},
        {"month": "T8/2026", "nhap": 300, "xuat": 270},
        {"month": "T9/2026", "nhap": 350, "xuat": 290},
    ]

    return {
        "success": True,
        "kpis": {
            "total_products": total_products,
            "total_suppliers": total_suppliers,
            "total_imports": total_imports,
            "total_exports": total_exports,
            "total_inventory_quantity": int(total_inventory_quantity),
            "estimated_inventory_value": int(estimated_inventory_value),
            "low_stock_count": low_stock_count
        },
        "top_exported_items": top_exported_items,
        "low_stock_warnings": low_stock_warnings,
        "monthly_chart": monthly_chart
    }
