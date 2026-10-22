# 03. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS)

---

## 1. YÊU CẦU BẢO MẬT (SECURITY)

- **Mật khẩu & Mã hóa**: Mật khẩu người dùng phải được băm bằng thuật toán `bcrypt` trước khi lưu vào CSDL. Không lưu mật khẩu ở dạng plain-text.
- **Xác thực & Phân quyền**: Sử dụng chuẩn JWT (JSON Web Token) với thời gian hết hạn (`exp`), chữ ký thuật toán `HS256`. API Endpoint phải được bảo vệ bởi middleware kiểm tra Bearer token và danh sách vai trò cho phép (`require_roles`).
- **An toàn Thông tin AI**:
  - Không truyền mật khẩu, token xác thực, hoặc dữ liệu tài chính nhạy cảm không cần thiết lên API AI (OpenAI).
  - API Key của OpenAI/Gemini phải được lưu trong biến môi trường `.env`, tuyệt đối không commit `.env` lên Git codebase.
- **Phòng chống Tấn công CSDL**: Sử dụng SQLAlchemy ORM Parametrized Queries chống lại SQL Injection 100%.

---

## 2. HIỆU NĂNG VÀ TÍNH TOÀN VẸN DỮ LIỆU (PERFORMANCE & INTEGRITY)

- **ACID Transactions**:
  - Mọi thao tác Nhập/Xuất kho phải được thực hiện trong 1 DB Transaction duy nhất.
  - Sử dụng khóa dòng (`with_for_update`) với các truy vấn xuất kho để ngăn ngừa xung đột dữ liệu khi có truy cập đồng thời (Race condition).
- **Thời gian Phản hồi (Latency)**:
  - Các API CRUD thông thường: Thời gian phản hồi < 200ms.
  - API Báo cáo & Dashboard: Thời gian phản hồi < 500ms.
  - API AI Analysis: Xử lý bất đồng bộ (Async API call) với timeout tối đa 15 giây, có cơ chế bắt lỗi timeout/rate-limit mượt mà.
- **Độ tin cậy (Reliability)**:
  - Bắt lỗi tập trung (Global Exception Handling) ở FastAPI, không để lọt Stack Trace hoặc lỗi unhandled ra cho người dùng cuối. Response trả về dạng JSON chuẩn dạng: `{"success": false, "message": "Nội dung lỗi"}`.

---

## 3. TÍNH KHẢ DỤNG VÀ THIẾT KẾ GIAO DIỆN (USABILITY & DESIGN)

- **Giao diện Chuyên nghiệp (Enterprise Dashboard Style)**:
  - Thiết kế hiện đại bằng Tailwind CSS + Lucide Icons + Recharts.
  - Bố cục Sidebar cố định, Topbar hiển thị tên người dùng và vai trò (Role Badge: Admin, Thủ kho, Kế toán).
  - Sử dụng Toast Notifications thông báo kết quả thao tác (Thành công/Lỗi) và Modal Dialog cho các form thêm/sửa/nhập/xuất.
- **Tính Tương thích (Compatibility)**: Responsive trên màn hình Desktop, Laptop và Tablet.
- **Khả năng Đóng gói & Triển khai (Deployment)**:
  - Đóng gói hoàn chỉnh bằng Docker Container & Docker Compose.
  - Có file `seed.py` khởi tạo dữ liệu ban đầu phục vụ báo cáo và demo môn học trong 1 click command.
