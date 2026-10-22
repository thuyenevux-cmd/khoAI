from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.product import Product
from app.models.inventory import Inventory
from app.models.receipt import (
    ImportReceipt,
    ExportReceipt,
    ImportReceiptDetail,
    ExportReceiptDetail
)

class WarehouseGroundingService:
    """
    Tập hợp các hàm nghiệp vụ an toàn để truy vấn dữ liệu kho từ CSDL.
    Mô hình AI chỉ nhận kết quả JSON đã được tổng hợp, kiểm tra và bảo mật.
    Tuyệt đối không cấp quyền truy cập SQL trực tiếp cho mô hình AI.
    """

    @staticmethod
    def get_low_stock_products(db: Session) -> List[Dict[str, Any]]:
        """Lấy danh sách các sản phẩm đang có tồn kho <= mức tồn tối thiểu."""
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        
        products = db.query(Product).join(Inventory).filter(
            Product.is_active == True,
            Inventory.quantity <= Product.minimum_stock
        ).all()

        results = []
        for p in products:
            exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
                ExportReceiptDetail.product_id == p.id,
                ExportReceipt.receipt_date >= thirty_days_ago
            ).scalar() or 0

            stock = p.inventory.quantity if p.inventory else 0
            results.append({
                "code": p.code,
                "name": p.name,
                "current_stock": stock,
                "minimum_stock": p.minimum_stock,
                "unit": p.unit.name if p.unit else "cái",
                "export_30_days": int(exp_30),
                "status": "Hết hàng" if stock == 0 else "Dưới tồn tối thiểu"
            })
        return results

    @staticmethod
    def get_product_stock_info(db: Session, query_str: str) -> List[Dict[str, Any]]:
        """Tra cứu chi tiết sản phẩm theo mã SKU hoặc từ khóa tên sản phẩm."""
        thirty_days_ago = datetime.now(timezone.utc) - timedelta(days=30)
        q = query_str.strip().lower()

        products = db.query(Product).filter(Product.is_active == True).all()
        matched = []

        for p in products:
            code_match = p.code.lower() in q or q in p.code.lower()
            name_words = [w for w in p.name.lower().split() if len(w) > 2]
            name_match = p.name.lower() in q or any(w in q for w in name_words)

            if code_match or name_match:
                stock = p.inventory.quantity if p.inventory else 0
                
                # Giá nhập gần nhất
                latest_detail = db.query(ImportReceiptDetail).filter(
                    ImportReceiptDetail.product_id == p.id
                ).order_by(ImportReceiptDetail.id.desc()).first()
                price = latest_detail.unit_price if latest_detail else 0.0

                exp_30 = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
                    ExportReceiptDetail.product_id == p.id,
                    ExportReceipt.receipt_date >= thirty_days_ago
                ).scalar() or 0

                burn_rate = round(exp_30 / 30.0, 2)
                days_left = round(stock / burn_rate, 1) if burn_rate > 0 else "Không xác định"

                matched.append({
                    "code": p.code,
                    "name": p.name,
                    "category": p.category.name if p.category else "Chung",
                    "unit": p.unit.name if p.unit else "cái",
                    "current_stock": stock,
                    "minimum_stock": p.minimum_stock,
                    "latest_price_vnd": int(price),
                    "estimated_total_value_vnd": int(stock * price),
                    "export_30_days": int(exp_30),
                    "burn_rate_per_day": burn_rate,
                    "estimated_days_of_stock": days_left,
                    "is_low_stock": stock <= p.minimum_stock
                })
        return matched

    @staticmethod
    def get_inventory_summary(db: Session, days: int = 30) -> Dict[str, Any]:
        """Tổng hợp chỉ số toàn kho trong khoảng thời gian xác định."""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)

        products = db.query(Product).filter(Product.is_active == True).all()
        total_items = len(products)
        total_stock = 0
        total_value = 0
        low_stock_count = 0

        for p in products:
            stock = p.inventory.quantity if p.inventory else 0
            total_stock += stock
            if stock <= p.minimum_stock:
                low_stock_count += 1

            latest_detail = db.query(ImportReceiptDetail).filter(
                ImportReceiptDetail.product_id == p.id
            ).order_by(ImportReceiptDetail.id.desc()).first()
            price = latest_detail.unit_price if latest_detail else 0.0
            total_value += int(stock * price)

        total_import = db.query(func.sum(ImportReceiptDetail.quantity)).join(ImportReceipt).filter(
            ImportReceipt.receipt_date >= start_date
        ).scalar() or 0

        total_export = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
            ExportReceipt.receipt_date >= start_date
        ).scalar() or 0

        return {
            "period": f"{days} ngày gần nhất",
            "total_products_managed": total_items,
            "total_units_in_stock": total_stock,
            "estimated_inventory_valuation_vnd": total_value,
            "low_stock_product_count": low_stock_count,
            "total_imported_quantity": int(total_import),
            "total_exported_quantity": int(total_export),
            "timestamp": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        }

    @staticmethod
    def get_top_exported_products(db: Session, days: int = 30, limit: int = 5) -> List[Dict[str, Any]]:
        """Lấy danh sách các mặt hàng có lượt xuất cao nhất trong kỳ."""
        start_date = datetime.now(timezone.utc) - timedelta(days=days)
        
        products = db.query(Product).filter(Product.is_active == True).all()
        items = []

        for p in products:
            stock = p.inventory.quantity if p.inventory else 0
            exp_qty = db.query(func.sum(ExportReceiptDetail.quantity)).join(ExportReceipt).filter(
                ExportReceiptDetail.product_id == p.id,
                ExportReceipt.receipt_date >= start_date
            ).scalar() or 0

            if exp_qty > 0:
                items.append({
                    "code": p.code,
                    "name": p.name,
                    "unit": p.unit.name if p.unit else "cái",
                    "current_stock": stock,
                    "exported_quantity": int(exp_qty),
                    "burn_rate_per_day": round(exp_qty / float(days), 2)
                })

        items.sort(key=lambda x: x["exported_quantity"], reverse=True)
        return items[:limit]

    @staticmethod
    def get_warehouse_business_guide() -> Dict[str, Any]:
        """Tài liệu nghiệp vụ chuẩn của hệ thống quản lý kho."""
        return {
            "huong_dan_tao_phieu_nhap": [
                "Bước 1: Vào thanh menu điều hướng chọn mục 'Nhập Kho'.",
                "Bước 2: Bấm nút '+ Tạo Phiếu Nhập'.",
                "Bước 3: Chọn Nhà cung cấp tương ứng và ngày chứng từ.",
                "Bước 4: Thêm các mặt hàng cần nhập, nhập số lượng và đơn giá nhập.",
                "Bước 5: Bấm 'Lưu Phiếu Nhập'. Hệ thống sẽ tự động cộng dồn số lượng vào bảng Tồn kho (inventories) và ghi nhận biến động (stock_movements)."
            ],
            "huong_dan_tao_phieu_xuat": [
                "Bước 1: Vào thanh menu điều hướng chọn mục 'Xuất Kho'.",
                "Bước 2: Bấm nút '+ Tạo Phiếu Xuất'.",
                "Bước 3: Điền lý do xuất (Bán lẻ, điều chuyển đại lý, xuất mẫu...).",
                "Bước 4: Chọn sản phẩm và nhập số lượng xuất.",
                "Bước 5: Bấm 'Lưu Phiếu Xuất'. Hệ thống kiểm tra điều kiện tồn kho thực tế trước khi ghi sổ."
            ],
            "nguyen_nhan_tu_choi_xuat_kho": [
                "1. Không đủ số lượng xuất kho: Số lượng xuất yêu cầu lớn hơn số lượng tồn kho khả dụng hiện tại (current_stock < requested_export_qty).",
                "2. Mặt hàng đã bị khóa hoặc ngừng kinh doanh: Cột is_active = False.",
                "3. Số lượng xuất nhập vào không hợp lệ (nhỏ hơn hoặc bằng 0, hoặc không phải số nguyên dương).",
                "4. Người dùng chưa đăng nhập hoặc không có phân quyền thủ kho (Role WAREHOUSE hoặc ADMIN)."
            ]
        }

    @classmethod
    def collect_grounding_context(cls, db: Session, question: str) -> Dict[str, Any]:
        """
        Phân loại ý định thông minh dựa trên từ khóa câu hỏi của người dùng
        và thu thập ngữ cảnh dữ liệu CSDL chính xác, gọn gàng, bảo mật.
        """
        q = question.lower().strip()
        context: Dict[str, Any] = {
            "system_time": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        }

        # 1. Tra cứu tồn kho cụ thể
        specific_products = cls.get_product_stock_info(db, q)
        if specific_products:
            context["product_search_results"] = specific_products

        # 2. Mặt hàng sắp hết / dưới mức an toàn / cần nhập thêm
        if any(w in q for w in ["sắp hết", "hết hàng", "cảnh báo", "tối thiểu", "cần nhập", "nhập thêm", "dưới mức", "bổ sung", "thiếu hàng"]):
            context["low_stock_alert_items"] = cls.get_low_stock_products(db)

        # 3. Phân tích nhập xuất / tổng quan toàn kho / định giá
        if any(w in q for w in ["tổng quan", "tháng này", "báo cáo", "tổng giá trị", "bao nhiêu tiền", "trị giá", "định giá", "tổng số", "tổng lượng"]):
            context["warehouse_summary_30_days"] = cls.get_inventory_summary(db, days=30)

        # 4. Top xuất kho / hàng bán chạy
        if any(w in q for w in ["bán chạy", "xuất nhiều", "top xuất", "chạy nhất", "tốc độ xuất", "tiêu thụ"]):
            context["top_exported_products"] = cls.get_top_exported_products(db, days=30, limit=5)

        # 5. Hướng dẫn nghiệp vụ / nguyên nhân từ chối
        if any(w in q for w in ["hướng dẫn", "tạo phiếu", "làm thế nào", "tại sao", "từ chối", "không đủ", "nguyên nhân", "cách nhập", "cách xuất"]):
            context["business_guidelines"] = cls.get_warehouse_business_guide()

        # Nếu chưa khớp ngữ cảnh nào hoặc câu hỏi rộng, luôn bổ sung tóm tắt cơ bản
        if len(context) == 1:
            context["warehouse_summary_30_days"] = cls.get_inventory_summary(db, days=30)
            context["low_stock_alert_items"] = cls.get_low_stock_products(db)[:5]

        return context

warehouse_grounding = WarehouseGroundingService()
