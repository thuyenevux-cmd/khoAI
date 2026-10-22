# BẢNG ĐỐI CHIẾU TIÊU CHÍ ĐÁNH GIÁ RUBRIC HỌC PHẦN AIA331
**Học phần:** Ứng dụng trí tuệ nhân tạo (AIA331) - **Mã số:** 80273  
**Đơn vị:** Trường Đại học Công nghệ Thông tin và Truyền thông (ICTU) - Đại học Thái Nguyên  
**Đề tài:** HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI (AI-POWERED INVENTORY MANAGEMENT SYSTEM)  
**Giảng viên hướng dẫn:** ThS. NGUYỄN TUẤN ANH  
**Sinh viên thực hiện:**  
1. Dương Minh Quang - MSV: `DTC245200225`  
2. Vũ Ngọc Anh Thuyên - MSV: `DTC245200428`  
**Lớp:** Công nghệ Thông tin - K24 ICTU  

---

## I. MA TRẬN 40 TIÊU CHÍ ĐÁNH GIÁ VÀ VỊ TRÍ MINH CHỨNG THỰC TẾ

| STT | Tiêu chí đánh giá Rubric AIA331 | Vị trí minh chứng trong báo cáo | Tệp mã nguồn / Bằng chứng thực nghiệm | Trạng thái |
| :---: | :--- | :--- | :--- | :---: |
| 01 | Khảo sát bối cảnh, đối tượng người dùng, quy trình nghiệp vụ kho | Chương 1, 3 | Có trong mã nguồn và báo cáo | **Đạt** |
| 02 | Đặc tả các yêu cầu chức năng (REQ-AUTH -> REQ-AUDIT) & phi chức năng | Chương 3 | Có trong mã nguồn và báo cáo | **Đạt** |
| 03 | Phân tích quy trình hệ thống qua Use Case Diagram chuẩn UML | Chương 3, Hình 3.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 04 | Mô hình hóa nghiệp vụ Đăng nhập qua Activity Diagram | Chương 4, Hình 4.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 05 | Mô hình hóa nghiệp vụ Nhập kho qua Activity Diagram | Chương 4, Hình 4.2 | Có trong mã nguồn và báo cáo | **Đạt** |
| 06 | Mô hình hóa nghiệp vụ Xuất kho chống âm qua Activity Diagram | Chương 4, Hình 4.3 | Có trong mã nguồn và báo cáo | **Đạt** |
| 07 | Mô hình hóa luồng xử lý AI qua Activity Diagram | Chương 4, Hình 4.4 | Có trong mã nguồn và báo cáo | **Đạt** |
| 08 | Thiết kế Cơ sở dữ liệu quan hệ chuẩn 3NF (11 bảng) | Chương 5, Bảng 5.1-5.11 | Có trong mã nguồn và báo cáo | **Đạt** |
| 09 | Sơ đồ thực thể liên kết ERD chuẩn hóa | Chương 5, Hình 5.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 10 | Khóa chính, khóa ngoại, ràng buộc toàn vẹn và Indexing tối ưu | Chương 5, ddl.sql | Có trong mã nguồn và báo cáo | **Đạt** |
| 11 | Mô hình kiến trúc tổng thể 3-Tier Client-Server | Chương 6, Hình 6.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 12 | Sơ đồ luồng dữ liệu DFD Mức 0 (Context Diagram) | Chương 6, Hình 6.2a | Có trong mã nguồn và báo cáo | **Đạt** |
| 13 | Sơ đồ luồng dữ liệu DFD Mức 1 (Chi tiết phân rã nghiệp vụ) | Chương 6, Hình 6.2b | Có trong mã nguồn và báo cáo | **Đạt** |
| 14 | Sơ đồ tuần tự Sequence Diagram cho quy trình Nhập kho | Chương 7, Hình 7.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 15 | Sơ đồ tuần tự Sequence Diagram cho quy trình Xuất kho | Chương 7, Hình 7.2 | Có trong mã nguồn và báo cáo | **Đạt** |
| 16 | Sơ đồ tuần tự Sequence Diagram cho quy trình Hỏi đáp AI NLP | Chương 8, Hình 8.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 17 | Thuật toán tính toán tồn an toàn và tốc độ tiêu thụ (Burn-rate) | Chương 8, Công thức (8.1) | Có trong mã nguồn và báo cáo | **Đạt** |
| 18 | Xử lý an toàn ngoại lệ chia cho 0 (ZeroDivisionError) khi sales=0 | Chương 8, Mã nguồn 8.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 19 | Cơ chế Strict Grounding Context chống ảo giác cho mô hình ngôn ngữ | Chương 8, Bảng 8.3 | Có trong mã nguồn và báo cáo | **Đạt** |
| 20 | Cơ chế Fallback tự động sang Rule Engine khi mất kết nối LLM | Chương 8, Bảng 8.4 | Có trong mã nguồn và báo cáo | **Đạt** |
| 21 | Kiến trúc Backend FastAPI, Pydantic Schemas và SQLAlchemy ORM | Chương 9 | Có trong mã nguồn và báo cáo | **Đạt** |
| 22 | Thiết kế hệ thống RESTful API chuẩn HTTP status codes | Chương 9, Bảng 9.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 23 | Quản lý phiên và phân quyền RBAC (ADMIN, WAREHOUSE, ACCOUNTANT) | Chương 9, 11 | Có trong mã nguồn và báo cáo | **Đạt** |
| 24 | Giao diện người dùng React Vite Responsive hiện đại | Chương 10, Hình 10.1-10.5 | Có trong mã nguồn và báo cáo | **Đạt** |
| 25 | Bảng điều khiển KPI Dashboard trực quan hóa số liệu thời gian thực | Chương 10, Hình 10.2 | Có trong mã nguồn và báo cáo | **Đạt** |
| 26 | Giao diện AI Hub phân tích báo cáo kho tự động | Chương 10, Hình 10.3 | Có trong mã nguồn và báo cáo | **Đạt** |
| 27 | Giao diện Trợ lý thông minh hỏi đáp bằng tiếng Việt tự nhiên | Chương 10, Hình 10.4 | Có trong mã nguồn và báo cáo | **Đạt** |
| 28 | Cơ chế bảo mật JWT Bearer Token với thuật toán mã hóa HS256 | Chương 11 | Có trong mã nguồn và báo cáo | **Đạt** |
| 29 | Mã hóa mật khẩu một chiều sử dụng thuật toán Argon2/Bcrypt | Chương 11 | Có trong mã nguồn và báo cáo | **Đạt** |
| 30 | Giao dịch CSDL đảm bảo tính ACID và Rollback khi xuất vượt tồn | Chương 11, Bảng 11.2 | Có trong mã nguồn và báo cáo | **Đạt** |
| 31 | Ghi nhật ký kiểm toán (Audit Trail) cho mọi biến động xuất nhập tồn | Chương 11 | Có trong mã nguồn và báo cáo | **Đạt** |
| 32 | Cấu hình biến môi trường an toàn qua .env / .env.example | Chương 12 | Có trong mã nguồn và báo cáo | **Đạt** |
| 33 | Quy trình đóng gói Docker container và triển khai hệ thống | Chương 12 | Có trong mã nguồn và báo cáo | **Đạt** |
| 34 | Chiến lược kiểm thử tự động Unit Test và Integration Test | Chương 13 | Có trong mã nguồn và báo cáo | **Đạt** |
| 35 | Bộ kịch bản kiểm thử 12 Test Cases bao phủ chức năng chính | Chương 13, Bảng 13.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 36 | Kết quả thực thi Pytest 100% Passed (12/12 test cases) | Chương 14, Bảng 14.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 37 | Đo lường định lượng độ trễ API (<100ms) và phản hồi AI (<1.5s) | Chương 14, Bảng 14.2 | Có trong mã nguồn và báo cáo | **Đạt** |
| 38 | Phân loại minh bạch 5 hạng mục: IMPLEMENTED, TESTED, PROPOSED... | Chương 15, Bảng 15.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 39 | Ma trận truy vết yêu cầu (Traceability Matrix) từ Req đến Test | Phụ lục A, Bảng A.1 | Có trong mã nguồn và báo cáo | **Đạt** |
| 40 | Định dạng báo cáo chuẩn ICTU (Font Times, lề, khung TikZ, caption) | Toàn bộ báo cáo | Có trong mã nguồn và báo cáo | **Đạt** |

---

## II. XÁC NHẬN CỦA NHÓM SINH VIÊN
Nhóm sinh viên cam kết đã rà soát nghiêm túc 40/40 tiêu chí trên, bảo đảm báo cáo phản ánh trung thực toàn bộ kết quả phát triển phần mềm và thực nghiệm trí tuệ nhân tạo của đồ án.
