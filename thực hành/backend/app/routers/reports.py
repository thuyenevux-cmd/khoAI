import io
import csv
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, Response, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.database import get_db
from app.models.product import Product
from app.models.receipt import ImportReceiptDetail, ExportReceiptDetail, ImportReceipt, ExportReceipt
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/reports", tags=["Inventory Reports Engine"])

@router.get("/inventory")
def get_inventory_report(
    period: Optional[str] = "30_DAYS", # 30_DAYS, THIS_MONTH, LAST_MONTH, ALL
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    now = datetime.now(timezone.utc)
    start_date = now - timedelta(days=30)
    if period == "THIS_MONTH":
        start_date = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
    elif period == "LAST_MONTH":
        first_of_this_month = datetime(now.year, now.month, 1, tzinfo=timezone.utc)
        last_month_end = first_of_this_month - timedelta(days=1)
        start_date = datetime(last_month_end.year, last_month_end.month, 1, tzinfo=timezone.utc)
    elif period == "ALL":
        start_date = datetime(2020, 1, 1, tzinfo=timezone.utc)

    products = db.query(Product).filter(Product.is_active == True).all()
    report_rows = []

    for p in products:
        ending_stock = p.inventory.quantity if p.inventory else 0

        # Total Import in period
        period_import = db.query(func.sum(ImportReceiptDetail.quantity)).join(ImportReceipt).filter(
            ImportReceiptDetail.product_id == p.id,
            ImportReceipt.receipt_date >= start_date
        ).scalar() or 0

        # Total Export in period
        period_export = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceiptDetail.product_id == p.id,
            ExportReceipt.receipt_date >= start_date
        ).scalar() or 0

        # Beginning Stock = Ending Stock - Period Import + Period Export
        beginning_stock = max(0, ending_stock - period_import + period_export)

        report_rows.append({
            "product_id": p.id,
            "product_code": p.code,
            "product_name": p.name,
            "category_name": p.category.name if p.category else "",
            "unit_name": p.unit.name if p.unit else "",
            "beginning_stock": int(beginning_stock),
            "import_quantity": int(period_import),
            "export_quantity": int(period_export),
            "ending_stock": int(ending_stock),
            "minimum_stock": p.minimum_stock,
            "status": "Dưới tồn tối thiểu" if ending_stock <= p.minimum_stock else "Bình thường"
        })

    return {
        "success": True,
        "period": period,
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": now.strftime("%Y-%m-%d"),
        "items": report_rows
    }

@router.get("/inventory/export-csv")
def export_inventory_csv(
    period: Optional[str] = "30_DAYS",
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    report_data = get_inventory_report(period=period, db=db, current_user=current_user)
    items = report_data["items"]

    output = io.StringIO()
    # UTF-8 BOM for Excel compatibility
    output.write('\ufeff')
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Mã sản phẩm", "Tên sản phẩm", "Nhóm hàng", "Đơn vị tính",
        "Tồn đầu kỳ", "Tổng nhập", "Tổng xuất", "Tồn cuối kỳ", "Tồn tối thiểu", "Trạng thái"
    ])

    for item in items:
        writer.writerow([
            item["product_code"],
            item["product_name"],
            item["category_name"],
            item["unit_name"],
            item["beginning_stock"],
            item["import_quantity"],
            item["export_quantity"],
            item["ending_stock"],
            item["minimum_stock"],
            item["status"]
        ])

    response = Response(content=output.getvalue(), media_type="text/csv")
    response.headers["Content-Disposition"] = f"attachment; filename=Bao_Cao_Kho_{period}_{datetime.now().strftime('%Y%m%d')}.csv"
    return response
