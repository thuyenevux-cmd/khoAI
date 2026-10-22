# 02. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS)

---

## 1. QUẢN LÝ TÀI KHOẢN VÀ PHÂN QUYỀN (RBAC)

- **FR-01**: Đăng nhập bằng tên tài khoản (username) và mật khẩu, trả về JWT Access Token.
- **FR-02**: Quản lý danh sách người dùng (Chỉ dành cho ADMIN): Thêm mới, chỉnh sửa thông tin, đổi vai trò, kích hoạt / khóa tài khoản.
- **FR-03**: Phân quyền hệ thống theo 3 vai trò:
  - **ADMIN (Quản trị)**: Toàn quyền truy cập tất cả tính năng backend và frontend.
  - **THỦ KHO (Warehouse)**: Xem danh mục sản phẩm/nhà cung cấp; Lập phiếu nhập kho; Lập phiếu xuất kho; Xem tồn kho; Xem lịch sử nhập xuất; Xem cảnh báo hàng dưới mức tối thiểu. Tuyệt đối không được truy cập quản lý người dùng và phân quyền.
  - **KẾ TOÁN (Accountant)**: Xem sản phẩm, nhà cung cấp, phiếu nhập, phiếu xuất, báo cáo xuất-nhập-tồn, chỉ số tài chính và phân tích AI. Không được tạo/chỉnh sửa phiếu nhập/xuất kho.

---

## 2. QUẢN LÝ DANH MỤC CƠ BẢN

- **FR-04 (Hàng hóa)**: CRUD thông tin Hàng hóa bao gồm: Mã hàng (Unique), Tên hàng, Nhóm hàng, Đơn vị tính, Mức tồn tối thiểu, Mô tả, Trạng thái (Soft-delete). Tìm kiếm theo tên/mã, lọc theo nhóm hàng, sắp xếp theo tên/tồn kho.
- **FR-05 (Nhóm hàng)**: CRUD Nhóm hàng (Mã nhóm, Tên nhóm, Mô tả).
- **FR-06 (Đơn vị tính)**: CRUD Đơn vị tính (Mã ĐVT, Tên ĐVT - Ví dụ: Cái, Hộp, Kg, Thùng, Chiếc).
- **FR-07 (Nhà cung cấp)**: CRUD Nhà cung cấp (Mã NCC, Tên NCC, Người liên hệ, Số điện thoại, Email, Địa chỉ, Ghi chú, Trạng thái).

---

## 3. QUẢN LÝ GIAO DỊCH KHO (TRANSACTIONS)

- **FR-08 (Lập Phiếu Nhập Kho)**:
  - Cho phép nhập mã phiếu, nhà cung cấp, ngày nhập, ghi chú và danh sách chi tiết hàng nhập (Mã hàng, Số lượng, Đơn giá nhập).
  - Tự động tính Thành tiền = Số lượng * Đơn giá.
  - Cập nhật tăng số lượng tồn kho `inventories.quantity = current_stock + import_qty` trong **DB Transaction**.
  - Tự động ghi nhận lịch sử vào `stock_movements`.
- **FR-09 (Lập Phiếu Xuất Kho)**:
  - Cho phép nhập mã phiếu, người nhận/bộ phận nhận, ngày xuất, ghi chú và chi tiết hàng xuất (Mã hàng, Số lượng xuất).
  - **Kiểm tra tồn kho trong Transaction bằng Row Lock**: Nếu `export_qty > current_stock`, lập tức từ chối và Rollback transaction. Ngăn chặn triệt để `current_stock < 0`.
  - Cập nhật giảm số lượng tồn kho `inventories.quantity = current_stock - export_qty`.
  - Ghi nhận lịch sử vào `stock_movements`.

---

## 4. THEO DÕI TỒN KHO & LỊCH SỬ GIAO DỊCH

- **FR-10 (Bảng Tồn Kho)**: Hiển thị Mã hàng, Tên hàng, Tồn đầu kỳ, Tổng nhập, Tổng xuất, Tồn cuối kỳ, Tồn tối thiểu và Trạng thái (Bình thường, Sắp hết, Dưới tồn tối thiểu, Hết hàng).
- **FR-11 (Cảnh báo Tồn Kho)**: Tự động phát hiện và đưa ra danh sách cảnh báo `current_stock <= minimum_stock`.
- **FR-12 (Lịch sử Nhập/Xuất & Audit Trail)**: Cho phép tra cứu nhật ký `stock_movements` lọc theo sản phẩm, loại giao dịch (IMPORT/EXPORT), khoảng ngày, nhà cung cấp, người thực hiện.

---

## 5. DASHBOARD & BÁO CÁO

- **FR-13 (Dashboard)**: Thống kê số lượng Tổng mặt hàng, Tổng nhà cung cấp, Số phiếu nhập, Số phiếu xuất, Số mặt hàng dưới tồn tối thiểu. Hiển thị biểu đồ xu hướng Nhập/Xuất kho theo tháng và Top hàng xuất chạy.
- **FR-14 (Báo cáo Xuất-Nhập-Tồn)**: Cho phép chọn khoảng thời gian (Tháng/Quý/Tùy chọn), xem bảng tổng hợp và xuất ra file CSV.

---

## 6. TÍCH HỢP TRÍ TUỆ NHÂN TẠO (AI FEATURES)

- **FR-15 (AI Sinh Báo cáo Kho)**: Nhận khoảng thời gian, truy vấn JSON snapshot dữ liệu thật từ CSDL, gửi tới AI Service (theo prompt template) để sinh báo cáo dạng văn bản nhận xét 4 phần: Tổng quan, Hàng cần chú ý, Bất thường, Khuyến nghị.
- **FR-16 (AI Gợi ý Nhập hàng)**: Phân tích Tồn hiện tại, Tồn tối thiểu, Tốc độ xuất (burn rate trong 30 ngày) để đưa ra đề xuất danh sách nhập hàng kèm mức ưu tiên (Cao/Trung bình/Thấp), lý do và số lượng gợi ý.
- **FR-17 (AI Phát hiện Biến động Bất thường)**: Nhận diện hiện tượng xuất/nhập tăng đột biến so với chu kỳ trước, hoặc sản phẩm tồn đọng lâu ngày không phát sinh giao dịch.
- **FR-18 (Hiển thị Dữ liệu Nguồn AI)**: Giao diện UI luôn có khoang hiển thị dữ liệu JSON gốc được trích xuất từ CSDL để minh bạch nguồn suy luận của AI.
