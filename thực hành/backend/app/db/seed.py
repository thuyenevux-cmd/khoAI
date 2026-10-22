from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.core.database import engine, Base, SessionLocal
from app.core.security import get_password_hash
from app.models import (
    User, Category, Unit, Supplier, Product, Inventory, StockMovement,
    ImportReceipt, ImportReceiptDetail, ExportReceipt, ExportReceiptDetail
)

def seed_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    try:
        # Check if users exist
        if db.query(User).first():
            print("Database already seeded. Skipping...")
            return

        print("Seeding initial database data...")

        # 1. Users
        admin_user = User(
            username="admin",
            password_hash=get_password_hash("Admin@123"),
            full_name="Quản Trị Viên Hệ Thống",
            role="ADMIN",
            is_active=True
        )
        warehouse_user = User(
            username="warehouse",
            password_hash=get_password_hash("Warehouse@123"),
            full_name="Thủ Kho Nguyen Van A",
            role="WAREHOUSE",
            is_active=True
        )
        accountant_user = User(
            username="accountant",
            password_hash=get_password_hash("Accountant@123"),
            full_name="Kế Toán Tran Thi B",
            role="ACCOUNTANT",
            is_active=True
        )
        db.add_all([admin_user, warehouse_user, accountant_user])
        db.commit()

        # 2. Categories
        cat1 = Category(code="CAT001", name="Thiết bị máy tính", description="Bàn phím, chuột, màn hình, RAM, SSD")
        cat2 = Category(code="CAT002", name="Văn phòng phẩm", description="Giấy in, bút, kẹp ghim, sổ tay")
        cat3 = Category(code="CAT003", name="Thiết bị mạng", description="Router, Switch, cáp mạng")
        cat4 = Category(code="CAT004", name="Phụ kiện điện tử", description="Tai nghe, bàn di chuột, cáp sạc")
        db.add_all([cat1, cat2, cat3, cat4])
        db.commit()

        # 3. Units
        unit_cai = Unit(code="UNIT001", name="Cái")
        unit_hop = Unit(code="UNIT002", name="Hộp")
        unit_kg = Unit(code="UNIT003", name="Kg")
        unit_thung = Unit(code="UNIT004", name="Thùng")
        unit_chiec = Unit(code="UNIT005", name="Chiếc")
        db.add_all([unit_cai, unit_hop, unit_kg, unit_thung, unit_chiec])
        db.commit()

        # 4. Suppliers
        sup1 = Supplier(
            code="SUP001", name="Công ty TNHH Phong Vũ", contact_person="Nguyễn Phong",
            phone="0901234567", email="phongvu@example.com", address="Hà Nội", status="ACTIVE"
        )
        sup2 = Supplier(
            code="SUP002", name="Nhà phân phối FPT Synnex", contact_person="Lê Synnex",
            phone="0912345678", email="synnex@fpt.com", address="TP. Hồ Chí Minh", status="ACTIVE"
        )
        sup3 = Supplier(
            code="SUP003", name="Thiết bị Văn phòng Hồng Hà", contact_person="Trần Hồng",
            phone="0923456789", email="hongha@vpp.com", address="Thái Nguyên", status="ACTIVE"
        )
        db.add_all([sup1, sup2, sup3])
        db.commit()

        # 5. Products
        products_data = [
            # code, name, cat, unit, min_stock, desc, initial_qty
            ("HH001", "Bàn phím cơ AKKO 3087", cat1.id, unit_cai.id, 10, "Bàn phím cơ Switch Pink", 5),
            ("HH002", "Chuột không dây Logitech M330", cat1.id, unit_cai.id, 15, "Chuột Silent chống ồn", 8),
            ("HH003", "Màn hình Dell Ultrasharp 24 inch", cat1.id, unit_cai.id, 5, "Màn hình đồ họa IPS", 20),
            ("HH004", "Giấy in A4 Double A 70gsm", cat2.id, unit_thung.id, 50, "Giấy in ram 500 tờ", 120),
            ("HH005", "Bút bi Thiên Long TL-027", cat2.id, unit_hop.id, 100, "Bút bi mực xanh", 0),
            ("HH006", "Router Wifi TP-Link Archer C6", cat3.id, unit_cai.id, 5, "Router Wifi AC1200", 12),
            ("HH007", "Cáp mạng Cat6 DINTEK 305m", cat3.id, unit_thung.id, 3, "Cuộn cáp mạng đồng", 2),
            ("HH008", "Tai nghe Gaming HyperX Cloud II", cat4.id, unit_cai.id, 8, "Tai nghe âm thanh 7.1", 15),
            ("HH009", "Ổ cứng SSD Samsung 980 500GB", cat1.id, unit_cai.id, 10, "SSD NVMe M.2 PCIe 3.0", 45),
            ("HH010", "RAM Kingston Fury 16GB DDR4", cat1.id, unit_cai.id, 10, "Bus 3200MHz tản nhiệt", 3),
            ("HH011", "Bàn di chuột Gaming RGB XL", cat4.id, unit_cai.id, 20, "Kích thước 800x300mm", 80),
            ("HH012", "Máy in HP LaserJet M211d", cat1.id, unit_cai.id, 2, "Máy in laser đơn năng", 5),
        ]

        created_products = {}
        for code, name, cat_id, unit_id, min_stock, desc, initial_qty in products_data:
            p = Product(
                code=code, name=name, category_id=cat_id, unit_id=unit_id,
                minimum_stock=min_stock, description=desc, is_active=True
            )
            db.add(p)
            db.flush()
            created_products[code] = p

            inv = Inventory(product_id=p.id, quantity=initial_qty)
            db.add(inv)

        db.commit()

        # 6. Historic Receipts & Stock Movements for Demo Real Data (e.g. HH001 25 exports in last 30 days)
        now = datetime.now(timezone.utc)
        past_15_days = now - timedelta(days=15)
        past_20_days = now - timedelta(days=20)

        # Import receipt 1 (HH001 +30 items 20 days ago)
        imp1 = ImportReceipt(
            receipt_code="PN20260901",
            supplier_id=sup1.id,
            created_by=warehouse_user.id,
            receipt_date=past_20_days,
            note="Nhập kho đầu tháng 9",
            status="COMPLETED"
        )
        db.add(imp1)
        db.flush()

        detail_imp1 = ImportReceiptDetail(
            receipt_id=imp1.id,
            product_id=created_products["HH001"].id,
            quantity=30,
            unit_price=850000.0
        )
        db.add(detail_imp1)

        mov_imp1 = StockMovement(
            product_id=created_products["HH001"].id,
            movement_type="IMPORT",
            reference_type="IMPORT_RECEIPT",
            reference_id=imp1.id,
            quantity=30,
            created_by=warehouse_user.id,
            created_at=past_20_days
        )
        db.add(mov_imp1)

        # Export receipt 1 (HH001 -25 items 15 days ago)
        exp1 = ExportReceipt(
            receipt_code="PX20260902",
            created_by=warehouse_user.id,
            receipt_date=past_15_days,
            receiver="Phòng Công nghệ Thông tin",
            note="Xuất trang bị phòng Lab máy tính",
            status="COMPLETED"
        )
        db.add(exp1)
        db.flush()

        detail_exp1 = ExportReceiptDetail(
            receipt_id=exp1.id,
            product_id=created_products["HH001"].id,
            quantity=25
        )
        db.add(detail_exp1)

        mov_exp1 = StockMovement(
            product_id=created_products["HH001"].id,
            movement_type="EXPORT",
            reference_type="EXPORT_RECEIPT",
            reference_id=exp1.id,
            quantity=25,
            created_by=warehouse_user.id,
            created_at=past_15_days
        )
        db.add(mov_exp1)

        db.commit()
        print("Database successfully seeded with demo accounts, categories, products, inventory, and receipt history!")

    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
