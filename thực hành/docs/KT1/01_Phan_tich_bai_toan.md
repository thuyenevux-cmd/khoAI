# 01. PHÂN TÍCH BÀI TOÁN QUẢN LÝ KHO TÍCH HỢP AI

**Đại học Thái Nguyên – Trường Đại học Công nghệ Thông tin và Truyền thông**  
**Học phần:** Ứng dụng trí tuệ nhân tạo – AIA331 | **Mã số:** 80273

---

## 1. ĐẶT VẤN ĐỀ VÀ THỰC TRẠNG

Đối với các doanh nghiệp vừa và nhỏ (SME), việc quản lý kho hàng hóa đóng vai trò sống còn đối với dòng tiền và hiệu quả vận hành. Tuy nhiên, thực trạng hiện nay tại hầu hết các đơn vị này vẫn còn gặp nhiều hạn chế:

- **Quản lý thủ công / Bảng tính (Excel/Google Sheets)**:
  - Dễ gặp sai sót do thao tác con người (nhập đè, xóa nhầm công thức).
  - Không có cơ chế khóa dòng (Row Locking) gây xung đột khi nhiều người cùng thao tác.
  - Thiếu khả năng kiểm soát số lượng tồn tối thiểu, dẫn đến việc đứt gãy nguồn cung hoặc tồn kho quá mức.
- **Thiếu khả năng truy vết (Audit Trail)**:
  - Không thể tra cứu chính xác ai là người lập phiếu nhập/xuất, thời gian thực hiện và lý do thay đổi số lượng.
  - Nguy cơ thất thoát vật tư, hàng hóa cao mà không tìm được nguyên nhân.
- **Rủi ro Tồn kho âm (Negative Stock)**:
  - Các hệ thống không có ràng buộc CSDL chặt chẽ cho phép xuất kho vượt quá số lượng hiện có, làm sai lệch toàn bộ báo cáo tài chính và kế toán.
- **Báo cáo chậm trễ & Thiếu góc nhìn dự báo**:
  - Việc tổng hợp báo cáo Nhập - Xuất - Tồn theo tháng mất nhiều thời gian.
  - Người quản lý không kịp thời phát hiện các biến động bất thường (hàng xuất tăng đột biến, hàng tồn lâu ngày) để đưa ra quyết định nhập hàng tối ưu.

---

## 2. GIẢI PHÁP ĐỀ XUẤT

Xây dựng **Hệ thống quản lý kho có tích hợp AI (AI-Powered Inventory Management System)** nhằm giải quyết triệt để các vấn đề trên thông qua:

1. **Chuẩn hóa quy trình nghiệp vụ số**: Quản lý toàn diện Sản phẩm, Nhóm hàng, Đơn vị tính, Nhà cung cấp, Phiếu nhập, Phiếu xuất và Tồn kho.
2. **Cơ chế Transaction CSDL khắt khe**:
   - Sử dụng ACID Transaction trong SQLAlchemy để đảm bảo việc tăng/giảm tồn kho và ghi lịch sử giao dịch (`stock_movements`) xảy ra đồng thời (Atomic).
   - Áp dụng Pessimistic Locking (`SELECT FOR UPDATE`) ngăn chặn tuyệt đối tình trạng tồn kho âm.
3. **Phân quyền truy cập dựa trên vai trò (RBAC)**:
   - Tách biệt rõ ràng 3 quyền: `ADMIN` (Quản trị hệ thống), `THỦ KHO` (Vận hành nhập/xuất), `KẾ TOÁN` (Xem báo cáo & tài chính).
4. **Tích hợp Trí tuệ nhân tạo (AI Engine)**:
   - **AI Sinh báo cáo kho theo tháng**: Tự động tổng hợp chỉ số và nhận xét tình trạng kho.
   - **AI Gợi ý nhập hàng**: Tính toán tốc độ xuất (burn rate) và cảnh báo mức ưu tiên nhập hàng kèm lý do rõ ràng.
   - **AI Phát hiện biến động bất thường**: Nhận diện hàng xuất/nhập đột biến hoặc hàng tồn đọng lâu ngày.
   - **Cam kết chống AI Hallucination**: AI chỉ phân tích dựa trên snapshot JSON dữ liệu thực tế được truy vấn từ CSDL, không tự bịa số liệu.

---

## 3. PHẠM VI DỰ ÁN

- **Phạm vi nghiệp vụ**: Quản lý kho nội bộ cho doanh nghiệp nhỏ.
- **Phạm vi công nghệ**:
  - Backend: Python 3.14 + FastAPI + SQLAlchemy ORM + Alembic + Pytest.
  - Frontend: React 18 + Vite + Tailwind CSS + Axios + Recharts.
  - CSDL: SQLite (phát triển local/testing) & MySQL 8.0 (Docker production).
  - AI Engine: OpenAI API (GPT-4o-mini) / Custom Offline AI Engine Interface.
