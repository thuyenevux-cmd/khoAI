# 02. HƯỚNG DẪN VÀ KỊCH BẢN DEMO BÁO CÁO MÔN HỌC (10 - 15 PHÚT)

**Học phần:** Ứng dụng trí tuệ nhân tạo – AIA331 | **Đề tài:** Hệ thống quản lý kho có tích hợp AI

---

## 🎭 KỊCH BẢN DEMO CHI TIẾT 10 BƯỚC

### 🔹 Bước 1: Đăng nhập tài khoản Quản trị viên (ADMIN)
- **Thao tác**: Mở trang Đăng nhập tại `http://localhost:3000/login`. Nhấn nút bấm nhanh tài khoản **ADMIN** (`admin` / `Admin@123`).
- **Minh chứng**: Đăng nhập thành công, hiển thị Badge màu đỏ `ADMIN` trên thanh Topbar và mở đủ 12 menu bên Sidebar (bao gồm Quản trị Người dùng).

### 🔹 Bước 2: Quản lý Danh mục Hàng hóa
- **Thao tác**: Vào menu `Quản lý Hàng hóa`. Tìm kiếm từ khóa `"AKKO"`.
- **Minh chứng**: Hiển thị mặt hàng `HH001 - Bàn phím cơ AKKO 3087` với **Tồn hiện tại = 5**, **Tồn tối thiểu = 10**.

### 🔹 Bước 3: Lập Phiếu Nhập Kho (Kiểm tra Tồn kho tăng)
- **Thao tác**: Vào menu `Phiếu Nhập kho` -> Bấm nút `LẬP PHIẾU NHẬP KHO`. Chọn Nhà cung cấp Phong Vũ. Chọn sản phẩm `HH001 - Bàn phím cơ` với **Số lượng nhập = 20**, Đơn giá = 850,000 đ -> Bấm `XÁC NHẬN NHẬP KHO`.
- **Minh chứng**: Phiếu nhập mã `PN...` được khởi tạo. Vào lại danh sách Hàng hóa / Tồn kho kiểm tra: Tồn kho `HH001` tăng từ **5 lên 25**.

### 🔹 Bước 4: Lập Phiếu Xuất Kho (Kiểm tra Tồn kho giảm)
- **Thao tác**: Vào menu `Phiếu Xuất kho` -> Bấm nút `LẬP PHIẾU XUẤT KHO`. Nhập người nhận `"Phòng Kế toán"`. Chọn mặt hàng `HH001` với **Số lượng xuất = 10** -> Bấm `XÁC NHẬN XUẤT KHO`.
- **Minh chứng**: Phiếu xuất mã `PX...` được tạo thành công. Kiểm tra lại Tồn kho `HH001` giảm từ **25 xuống 15**.

### 🔹 Bước 5: THỬ XUẤT VƯỢT TỒN KHO (Kiểm tra Chống Tồn kho âm)
- **Thao tác**: Tiếp tục bấm `LẬP PHIẾU XUẤT KHO`. Chọn sản phẩm `HH001` (Tồn kho hiện tại = 15). Nhập số lượng xuất = **9999** -> Bấm `XÁC NHẬN XUẤT KHO`.
- **Minh chứng khắt khe**: Hệ thống lập tức từ chối, hiển thị Banner cảnh báo màu đỏ: *"Số lượng tồn kho sản phẩm 'Bàn phím cơ AKKO 3087' (Mã: HH001) không đủ để xuất! (Tồn hiện tại: 15, Yêu cầu xuất: 9999)"*. CSDL tự động Rollback, tồn kho giữ nguyên 15.

### 🔹 Bước 6: Xem Cảnh báo Tồn dưới Mức Tối thiểu & Tra cứu Lịch sử
- **Thao tác**:
  - Đăng xuất -> Đăng nhập tài khoản **THỦ KHO** (`warehouse` / `Warehouse@123`).
  - Vào menu `Theo dõi Tồn kho` -> Chọn bộ lọc `CẢNH BÁO SẮP HẾT`.
  - Vào menu `Lịch sử Nhập / Xuất` -> Tra cứu nhật ký Audit Log ghi nhận chính xác toàn bộ 2 giao dịch nhập/xuất vừa thực hiện.

### 🔹 Bước 7: Xem Báo cáo Xuất - Nhập - Tồn & Tải CSV
- **Thao tác**: Đăng nhập tài khoản **KẾ TOÁN** (`accountant` / `Accountant@123`). Vào menu `Báo cáo Xuất-Nhập-Tồn`.
- **Minh chứng**: Bảng báo cáo hiển thị chuẩn Tồn đầu kỳ, Tổng nhập, Tổng xuất, Tồn cuối kỳ. Bấm nút `XUẤT BÁO CÁO CSV` -> Tải file Excel/CSV về máy thành công.

### 🔹 Bước 8: Chạy AI Feature 1 – AI Sinh Báo Cáo Kho Theo Tháng
- **Thao tác**: Vào menu `Phân tích AI Pro` -> Chọn Tab 1 `1. Báo Cáo Kho AI`.
- **Minh chứng**: AI phân tích và xuất văn bản Markdown 4 phần (Tình trạng kho, Hàng cần chú ý, Bất thường, Khuyến nghị). Mở khoang `Dữ liệu Nguồn CSDL` xem JSON snapshot đối chứng.

### 🔹 Bước 9: Chạy AI Feature 2 – AI Gợi Ý Nhập Hàng
- **Thao tác**: Bấm sang Tab 2 `2. Gợi Ý Nhập Hàng AI`.
- **Minh chứng**: AI hiển thị bảng Gợi ý nhập hàng phân cấp mức Ưu tiên (🔴 CAO, 🟡 TRUNG BÌNH, 🟢 THẤP) kèm Số lượng đề xuất tham khảo và lý do bám sát số liệu burn rate 30 ngày.

### 🔹 Bước 10: Chạy AI Feature 3 – AI Phân Tích Biến Động Bất Thường
- **Thao tác**: Bấm sang Tab 3 `3. Phân Tích Bất Thường AI`.
- **Minh chứng**: AI nhận diện chính xác các sản phẩm xuất tăng đột biến hoặc có nguy cơ đứt gãy cung ứng.
