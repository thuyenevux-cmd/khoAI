# KT2 - 01. KIẾN TRÚC SOURCE CODE BACKEND VÀ FRONTEND

---

## 1. BACKEND ARCHITECTURE (FASTAPI + PYTHON)

- **Entry Point**: `backend/app/main.py`
- **Configuration**: `backend/app/core/config.py` (Lưu cài đặt biến môi trường `.env`, JWT Secret Key, OpenAI Key)
- **Database Connection**: `backend/app/core/database.py` (Khởi tạo SQLAlchemy engine, SessionLocal factory)
- **Security**: `backend/app/core/security.py` (Hàm mã hóa băm mật khẩu `bcrypt`, sinh và kiểm tra JWT Access Token)
- **ORM Models (`backend/app/models/`)**: `User`, `Category`, `Unit`, `Supplier`, `Product`, `Inventory`, `ImportReceipt`, `ImportReceiptDetail`, `ExportReceipt`, `ExportReceiptDetail`, `StockMovement`.
- **Validation Schemas (`backend/app/schemas/`)**: Pydantic v2 schemas định nghĩa đầu vào/đầu ra chuẩn hóa cho REST API.
- **REST Routers (`backend/app/routers/`)**:
  - `auth.py`: Đăng nhập `/api/auth/login`, Lấy thông tin cá nhân `/api/auth/me`, Quản lý tài khoản `/api/auth/users`.
  - `categories.py`, `units.py`, `suppliers.py`, `products.py`: CRUD danh mục nền tảng.
  - `imports.py`: ACID Transaction nhập kho.
  - `exports.py`: ACID Transaction xuất kho + Row Lock + Chống tồn âm.
  - `inventory.py`: Tra cứu tồn kho & Cảnh báo tồn dưới mức tối thiểu.
  - `stock_movements.py`: Nhật ký truy vết Audit Log.
  - `dashboard.py`: Thống kê KPI & Dữ liệu biểu đồ.
  - `reports.py`: Báo cáo Xuất-Nhập-Tồn & Export CSV.
  - `ai.py`: APIs phân tích AI (Báo cáo, Gợi ý, Bất thường).

---

## 2. FRONTEND ARCHITECTURE (REACT + VITE)

- **Entry Point**: `frontend/src/main.jsx`
- **Routing**: `frontend/src/App.jsx` (React Router v6 + PrivateRoute guard theo vai trò)
- **Auth Context**: `frontend/src/contexts/AuthContext.jsx` (Lưu state người dùng và Token trong LocalStorage)
- **API Client**: `frontend/src/services/api.js` (Axios Interceptors tự động đính kèm `Bearer {token}`)
- **Layout**: `frontend/src/layouts/MainLayout.jsx` (Sidebar rẽ nhánh menu theo Role + Header hiển thị Badge vai trò)
- **Pages (`frontend/src/pages/`)**: `LoginPage`, `DashboardPage`, `ProductsPage`, `CategoriesPage`, `UnitsPage`, `SuppliersPage`, `ImportReceiptsPage`, `ExportReceiptsPage`, `InventoryPage`, `StockHistoryPage`, `ReportsPage`, `AIAnalysisPage`, `UsersPage`.
