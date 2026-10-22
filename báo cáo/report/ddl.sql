-- ==============================================================================
-- DDL KHỞI TẠO CƠ SỞ DỮ LIỆU QUAN HỆ CHUẨN 3NF
-- Đề tài: HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI (AI-Powered Inventory Management)
-- Học phần: Ứng dụng trí tuệ nhân tạo (AIA331) - Mã số: 80273 - ICTU 2026
-- ==============================================================================

-- 1. Bảng người dùng và phân quyền RBAC
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL CHECK(role IN ('ADMIN', 'WAREHOUSE', 'ACCOUNTANT')),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Bảng nhóm ngành hàng (Categories)
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Bảng đơn vị tính quy chuẩn (Units)
CREATE TABLE IF NOT EXISTS units (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(50) NOT NULL,
    description TEXT
);

-- 4. Bảng nhà cung cấp đối tác (Suppliers)
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    contact_person VARCHAR(100),
    phone VARCHAR(20),
    email VARCHAR(100),
    address TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 5. Bảng danh mục sản phẩm (Products)
CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(200) NOT NULL,
    category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE RESTRICT,
    unit_id INTEGER NOT NULL REFERENCES units(id) ON DELETE RESTRICT,
    cost_price NUMERIC(15,2) NOT NULL CHECK(cost_price >= 0),
    selling_price NUMERIC(15,2) NOT NULL CHECK(selling_price >= 0),
    minimum_stock INTEGER DEFAULT 0 CHECK(minimum_stock >= 0),
    maximum_stock INTEGER DEFAULT 0 CHECK(maximum_stock >= 0),
    location VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 6. Bảng tồn kho thời gian thực (Inventory)
CREATE TABLE IF NOT EXISTS inventory (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL UNIQUE REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL DEFAULT 0 CHECK(quantity >= 0),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 7. Bảng phiếu nhập kho (Import Receipts)
CREATE TABLE IF NOT EXISTS import_receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    supplier_id INTEGER NOT NULL REFERENCES suppliers(id) ON DELETE RESTRICT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    receipt_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    total_amount NUMERIC(15,2) DEFAULT 0.0 CHECK(total_amount >= 0),
    status VARCHAR(20) DEFAULT 'COMPLETED',
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 8. Bảng chi tiết phiếu nhập kho (Import Receipt Details)
CREATE TABLE IF NOT EXISTS import_receipt_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL REFERENCES import_receipts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price NUMERIC(15,2) NOT NULL CHECK(unit_price >= 0),
    total_price NUMERIC(15,2) NOT NULL CHECK(total_price >= 0)
);

-- 9. Bảng phiếu xuất kho (Export Receipts)
CREATE TABLE IF NOT EXISTS export_receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(50) NOT NULL UNIQUE,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    receipt_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    receiver VARCHAR(150) NOT NULL,
    total_amount NUMERIC(15,2) DEFAULT 0.0 CHECK(total_amount >= 0),
    status VARCHAR(20) DEFAULT 'COMPLETED',
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 10. Bảng chi tiết phiếu xuất kho (Export Receipt Details)
CREATE TABLE IF NOT EXISTS export_receipt_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    receipt_id INTEGER NOT NULL REFERENCES export_receipts(id) ON DELETE CASCADE,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price NUMERIC(15,2) NOT NULL CHECK(unit_price >= 0),
    total_price NUMERIC(15,2) NOT NULL CHECK(total_price >= 0)
);

-- 11. Bảng sổ cái nhật ký biến động kho kiểm toán (Stock Movements / Audit Trail)
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE RESTRICT,
    movement_type VARCHAR(20) NOT NULL CHECK(movement_type IN ('IMPORT', 'EXPORT', 'ADJUST')),
    quantity INTEGER NOT NULL,
    previous_stock INTEGER NOT NULL CHECK(previous_stock >= 0),
    new_stock INTEGER NOT NULL CHECK(new_stock >= 0),
    reference_id INTEGER,
    reference_type VARCHAR(50),
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE RESTRICT,
    note TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chỉ mục tối ưu hóa truy vấn hiệu năng cao (Indexing)
CREATE INDEX IF NOT EXISTS idx_products_code ON products(code);
CREATE INDEX IF NOT EXISTS idx_products_category ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_inventory_product ON inventory(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_product ON stock_movements(product_id);
CREATE INDEX IF NOT EXISTS idx_stock_movements_created ON stock_movements(created_at);
CREATE INDEX IF NOT EXISTS idx_import_receipts_date ON import_receipts(receipt_date);
CREATE INDEX IF NOT EXISTS idx_export_receipts_date ON export_receipts(receipt_date);
