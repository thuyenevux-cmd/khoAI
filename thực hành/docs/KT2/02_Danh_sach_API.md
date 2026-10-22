# KT2 - 02. DANH SÁCH RESTFUL API ENDPOINTS

---

## 1. XÁC THỰC VÀ QUẢN TRỊ NGUỜI DÙNG (/api/auth)

| Method | Endpoint | Yêu cầu Auth | Role cho phép | Mô tả |
| :--- | :--- | :---: | :--- | :--- |
| `POST` | `/api/auth/login` | ❌ No | Public | Đăng nhập trả về JWT Access Token |
| `GET` | `/api/auth/me` | ✅ Yes | ALL | Lấy thông tin tài khoản hiện tại |
| `GET` | `/api/auth/users` | ✅ Yes | ADMIN | Danh sách toàn bộ tài khoản |
| `POST` | `/api/auth/users` | ✅ Yes | ADMIN | Tạo tài khoản người dùng mới |
| `PUT` | `/api/auth/users/{id}` | ✅ Yes | ADMIN | Cập nhật / Khóa tài khoản người dùng |

---

## 2. DANH MỤC CƠ BẢN

| Method | Endpoint | Role cho phép | Mô tả |
| :--- | :--- | :--- | :--- |
| `GET/POST/PUT/DELETE` | `/api/categories` | ADMIN (CRUD), WH/ACC (View) | Quản lý Nhóm hàng hóa |
| `GET/POST/DELETE` | `/api/units` | ADMIN (CRUD), WH/ACC (View) | Quản lý Đơn vị tính |
| `GET/POST/PUT/DELETE` | `/api/suppliers` | ADMIN (CRUD), WH/ACC (View) | Quản lý Nhà cung cấp |
| `GET/POST/PUT/DELETE` | `/api/products` | ADMIN (CRUD), WH/ACC (View) | Quản lý Sản phẩm & Mức tồn min |

---

## 3. GIAO DỊCH KHO & TRUY VẾT

| Method | Endpoint | Role cho phép | Mô tả |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/imports` | ALL | Danh sách phiếu nhập kho |
| `POST` | `/api/imports` | ADMIN, WAREHOUSE | Lập phiếu nhập kho (Atomic Stock Increase) |
| `GET` | `/api/exports` | ALL | Danh sách phiếu xuất kho |
| `POST` | `/api/exports` | ADMIN, WAREHOUSE | Lập phiếu xuất kho (Lock row + Anti-Negative Stock) |
| `GET` | `/api/inventory` | ALL | Danh sách tồn kho thời gian thực |
| `GET` | `/api/inventory/alerts` | ALL | Danh sách cảnh báo hàng dưới mức tối thiểu |
| `GET` | `/api/stock-movements` | ALL | Nhật ký truy vết Audit Log giao dịch |

---

## 4. DASHBOARD, BÁO CÁO VÀ AI ANALYTICS

| Method | Endpoint | Role cho phép | Mô tả |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/dashboard` | ALL | Chỉ số KPI & Dữ liệu biểu đồ |
| `GET` | `/api/reports/inventory` | ALL | Bảng báo cáo Xuất-Nhập-Tồn |
| `GET` | `/api/reports/inventory/export-csv` | ALL | Tải báo cáo định dạng CSV |
| `POST` | `/api/ai/inventory-report` | ALL | AI Sinh báo cáo kho theo tháng |
| `POST` | `/api/ai/restock-recommendation`| ALL | AI Gợi ý kế hoạch nhập hàng |
| `POST` | `/api/ai/anomaly-summary` | ALL | AI Phân tích biến động bất thường |
