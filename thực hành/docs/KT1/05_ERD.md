# 05. SƠ ĐỒ THỰC THỂ LIÊN KẾT (ERD DIAGRAM)

---

## 1. MÔ TẢ CÁC BẢNG CƠ SỞ DỮ LIỆU

1. `users`: Lưu trữ tài khoản đăng nhập, mật khẩu mã hóa bcrypt, vai trò (ADMIN, WAREHOUSE, ACCOUNTANT).
2. `categories`: Lưu trữ nhóm hàng hóa (Thiết bị máy tính, Văn phòng phẩm,...).
3. `units`: Lưu trữ đơn vị tính (Cái, Hộp, Kg, Thùng, Chiếc,...).
4. `suppliers`: Lưu trữ thông tin nhà cung cấp sản phẩm.
5. `products`: Lưu trữ thông tin hàng hóa, liên kết FK đến `categories` và `units`, có cột `minimum_stock` lưu trữ mức tồn tối thiểu.
6. `import_receipts`: Lưu thông tin đầu phiếu nhập (Mã phiếu, NCC, người tạo, ngày nhập).
7. `import_receipt_details`: Lưu chi tiết các dòng mặt hàng nhập (Sản phẩm, số lượng nhập, đơn giá).
8. `export_receipts`: Lưu thông tin đầu phiếu xuất (Mã phiếu, người nhận, người tạo, ngày xuất).
9. `export_receipt_details`: Lưu chi tiết các dòng mặt hàng xuất (Sản phẩm, số lượng xuất).
10. `inventories`: Bảng tồn kho thời gian thực liên kết 1-1 với `products`, lưu `quantity` tồn hiện tại.
11. `stock_movements`: Bảng nhật ký giao dịch phục vụ truy vết audit log (Sản phẩm, loại giao dịch IMPORT/EXPORT, mã tham chiếu, số lượng biến động, người thực hiện, thời gian).

---

## 2. BIỂU ĐỒ ERD (MERMAID ERD)

```mermaid
erDiagram
    users ||--o{ import_receipts : "created_by"
    users ||--o{ export_receipts : "created_by"
    users ||--o{ stock_movements : "created_by"

    categories ||--o{ products : "belongs_to"
    units ||--o{ products : "measured_by"
    suppliers ||--o{ import_receipts : "supplied_by"

    products ||--|| inventories : "has_stock"
    products ||--o{ import_receipt_details : "included_in_import"
    products ||--o{ export_receipt_details : "included_in_export"
    products ||--o{ stock_movements : "tracked_in"

    import_receipts ||--|{ import_receipt_details : "contains"
    export_receipts ||--|{ export_receipt_details : "contains"

    users {
        int id PK
        string username UK
        string password_hash
        string full_name
        string role
        boolean is_active
        datetime created_at
    }

    categories {
        int id PK
        string code UK
        string name
        string description
    }

    units {
        int id PK
        string code UK
        string name
    }

    suppliers {
        int id PK
        string code UK
        string name
        string contact_person
        string phone
        string email
        string address
    }

    products {
        int id PK
        string code UK
        string name
        int category_id FK
        int unit_id FK
        int minimum_stock
        string description
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    inventories {
        int id PK
        int product_id FK_UK
        int quantity
        datetime updated_at
    }

    import_receipts {
        int id PK
        string receipt_code UK
        int supplier_id FK
        int created_by FK
        datetime receipt_date
        string note
        string status
    }

    import_receipt_details {
        int id PK
        int receipt_id FK
        int product_id FK
        int quantity
        float unit_price
    }

    export_receipts {
        int id PK
        string receipt_code UK
        int created_by FK
        datetime receipt_date
        string receiver
        string note
        string status
    }

    export_receipt_details {
        int id PK
        int receipt_id FK
        int product_id FK
        int quantity
    }

    stock_movements {
        int id PK
        int product_id FK
        string movement_type
        string reference_type
        int reference_id
        int quantity
        int created_by FK
        datetime created_at
    }
```

---

## 3. RÀNG BUỘC TOÀN VẸN CSDL (CONSTRAINTS)

- **Primary Keys**: Mỗi bảng có khóa chính tự tăng `id`.
- **Foreign Keys**: Ngăn chặn xóa dữ liệu cha gây mồ côi (Ví dụ: Không được xóa Product khi đã phát sinh phiếu nhập/xuất trong `import_receipt_details` / `export_receipt_details`).
- **Unique Indexes**: `users.username`, `categories.code`, `units.code`, `suppliers.code`, `products.code`, `import_receipts.receipt_code`, `export_receipts.receipt_code`.
- **Check Constraints**:
  - `import_receipt_details.quantity > 0`
  - `export_receipt_details.quantity > 0`
  - `inventories.quantity >= 0` (Ngăn ngừa tồn âm tại mức CSDL).
