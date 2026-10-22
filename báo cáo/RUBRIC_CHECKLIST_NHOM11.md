# BẢNG ĐỐI CHIẾU 40 TIÊU CHÍ RUBRIC ĐÁNH GIÁ ĐỒ ÁN
## HỌC PHẦN: ỨNG DỤNG TRÍ TUỆ NHÂN TẠO – AIA331 (MÃ: 80273)
### ĐỀ TÀI: HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI
**Giảng viên hướng dẫn:** ThS. Nguyễn Tuấn Anh  
**Nhóm thực hiện:** Nhóm 11  
- Dương Minh Quang – MSV: DTC245200225 (50%)
- Vũ Ngọc Anh Thuyên – MSV: DTC245200428 (50%)

---

| STT | Giai đoạn | Tiêu chí đánh giá (Rubric) | Hiện thực trong Project Nhóm 11 | Trạng thái |
|---|---|---|---|---|
| 1 | KT1 | 1.1 Khảo sát bài toán nghiệp vụ kho | Tài liệu khảo sát chi tiết quy trình nhập/xuất, vị trí kệ, tồn an toàn | ĐẠT (10/10) |
| 2 | KT1 | 1.2 Yêu cầu chức năng (FRs) | Đặc tả đầy đủ 9 nhóm tính năng (Auth, RBAC, CRUD SP, Kho, AI, NLP, Audit) | ĐẠT (10/10) |
| 3 | KT1 | 1.3 Yêu cầu phi chức năng (NFRs) | Chuẩn bảo mật OWASP, hiệu năng <100ms, toàn vẹn giao dịch ACID | ĐẠT (10/10) |
| 4 | KT1 | 1.4 Danh sách tác nhân (Actors) | 3 tác nhân rõ ràng: Admin, Thủ kho (Warehouse), Kế toán (Accountant) | ĐẠT (10/10) |
| 5 | KT1 | 1.5 Sơ đồ Use Case tổng thể | Bản vẽ `02_so_do_usecase_tong_the.png` và file `.drawio` tương ứng | ĐẠT (10/10) |
| 6 | KT1 | 1.6 Sơ đồ thực thể liên kết (ERD) | Bản vẽ `03_so_do_erd_11_bang.png` chuẩn hóa 3NF với 11 bảng | ĐẠT (10/10) |
| 7 | KT1 | 1.7 Thiết kế kiến trúc hệ thống | Bản vẽ kiến trúc 3 tầng `01_so_do_kien_truc_he_thong.png` | ĐẠT (10/10) |
| 8 | KT1 | 1.8 Xác định vị trí tích hợp AI | AI Hub tại Tầng ứng dụng phân tích dữ liệu kho & Chat NLP | ĐẠT (10/10) |
| 9 | KT1 | 1.9 Thiết kế Prompt AI có cấu trúc | System Prompt chặt chẽ chống ảo giác (Anti-Hallucination) | ĐẠT (10/10) |
| 10 | KT1 | 1.10 Kế hoạch thực hiện dự án | Bảng phân công chi tiết công việc 50% - 50% giữa 2 sinh viên | ĐẠT (10/10) |
| 11 | KT2 | 2.1 Cấu trúc mã nguồn Back-end | Clean Architecture: core, db, models, schemas, routers, services | ĐẠT (10/10) |
| 12 | KT2 | 2.2 Framework & Ngôn ngữ Back-end | FastAPI Async hiệu năng cao trên nền Python 3.14 | ĐẠT (10/10) |
| 13 | KT2 | 2.3 Quản lý kết nối Cơ sở dữ liệu | SQLAlchemy 2.0 ORM Session, SQLite/PostgreSQL, Alembic | ĐẠT (10/10) |
| 14 | KT2 | 2.4 Xác thực người dùng an toàn | OAuth2 Bearer Token, JSON Web Token (JWT) có thời hạn | ĐẠT (10/10) |
| 15 | KT2 | 2.5 Băm mật khẩu một chiều | Passlib với thuật toán Argon2/Bcrypt chống tấn công vét cạn | ĐẠT (10/10) |
| 16 | KT2 | 2.6 Kiểm soát phân quyền (RBAC) | Decorator phân quyền 3 cấp Admin / Warehouse / Accountant | ĐẠT (10/10) |
| 17 | KT2 | 2.7 API Danh mục & Sản phẩm | Bộ API RESTful CRUD chuẩn cho sản phẩm, NCC, vị trí kệ | ĐẠT (10/10) |
| 18 | KT2 | 2.8 API Giao dịch Nhập kho | Tạo phiếu nhập, phân bổ kệ, cộng dồn tồn an toàn | ĐẠT (10/10) |
| 19 | KT2 | 2.9 API Giao dịch Xuất kho | Kiểm tra số lượng tồn khả dụng, khóa dòng, trừ tồn tự động | ĐẠT (10/10) |
| 20 | KT2 | 2.10 Nhật ký kiểm toán (Audit Log) | Tự động ghi vết sự kiện bảng `audit_logs` có old/new values | ĐẠT (10/10) |
| 21 | KT3 | 3.1 Tích hợp mô hình AI LLM | Kết nối Google Gemini API (`gemini-1.5-flash` / `gemini-2.0`) | ĐẠT (10/10) |
| 22 | KT3 | 3.2 Ground-Truth Context Injection | Bơm trực tiếp dữ liệu tồn kho JSON thực tế vào prompt | ĐẠT (10/10) |
| 23 | KT3 | 3.3 Cơ chế Dự phòng kép (Fallback) | Bộ máy tính toán cục bộ (Local Rule Engine) hoạt động Offline | ĐẠT (10/10) |
| 24 | KT3 | 3.4 Thuật toán tính Burn-Rate | Công thức: Vận tốc V = Tổng xuất 30 ngày / 30 | ĐẠT (10/10) |
| 25 | KT3 | 3.5 Thuật toán tính Depletion Days | Số ngày cạn tồn = Tồn kho / V, loại bỏ hoàn toàn lỗi chia 0 | ĐẠT (10/10) |
| 26 | KT3 | 3.6 Phát hiện bất thường biến động | Thuật toán kiểm định thống kê Z-score và Outlier threshold | ĐẠT (10/10) |
| 27 | KT3 | 3.7 Trợ lý hỏi đáp NLP kho | Endpoint `POST /api/ai/ask` hỗ trợ hỏi đáp bằng ngôn ngữ tự nhiên | ĐẠT (10/10) |
| 28 | KT3 | 3.8 Định dạng dữ liệu đầu ra AI | Markdown Table kết hợp JSON data snapshot chứng minh | ĐẠT (10/10) |
| 29 | KT3 | 3.9 Thử nghiệm Prompt nhiều tình huống | Thử nghiệm Zero-shot, Few-shot, mặt hàng không xuất, cháy hàng | ĐẠT (10/10) |
| 30 | KT3 | 3.10 Ghi nhật ký truy vấn AI | Bảng `ai_query_logs` theo dõi thời gian phản hồi (ms) và prompt | ĐẠT (10/10) |
| 31 | Cuối kỳ | 4.1 Cấu trúc mã nguồn Front-end | React 18 SPA với Vite, Tailwind CSS, chia components/pages rõ ràng | ĐẠT (10/10) |
| 32 | Cuối kỳ | 4.2 Thiết kế UI/UX hiện đại | Giao diện SaaS Dark Mode lấy cảm hứng từ HorizonX / 21st.dev | ĐẠT (10/10) |
| 33 | Cuối kỳ | 4.3 Dashboard tổng quan KPI | 6 thẻ chỉ số: Tổng SP, Nhập, Xuất, Tồn kho, Định giá tiền VNĐ | ĐẠT (10/10) |
| 34 | Cuối kỳ | 4.4 Smart Table & LED Badge | Phân tích Markdown thành bảng có đèn LED nhấp nháy, nút Tạo phiếu | ĐẠT (10/10) |
| 35 | Cuối kỳ | 4.5 AI Chat Console trực quan | Hộp thoại Trợ lý hỏi đáp thông minh với 5 câu hỏi gợi ý nhanh | ĐẠT (10/10) |
| 36 | Cuối kỳ | 4.6 Bộ kiểm thử tự động (Unit Tests) | Bộ Pytest 12/12 kiểm thử tự động đạt tỷ lệ 100% Passed | ĐẠT (10/10) |
| 37 | Cuối kỳ | 4.7 Bộ sơ đồ kỹ thuật & Draw.io | 10 bản vẽ PNG độ nét cao + 10 file mã nguồn `.drawio` mở sửa được | ĐẠT (10/10) |
| 38 | Cuối kỳ | 4.8 Báo cáo Word chuẩn quy cách | File `báo cáo dự án Kho AI nhóm 11.docx` chuẩn lề 3-2-2-2, logo ICTU | ĐẠT (10/10) |
| 39 | Cuối kỳ | 4.9 Bộ mã nguồn LaTeX đầy đủ | Thư mục `latex/` sẵn sàng biên dịch XeLaTeX hoặc nộp Overleaf | ĐẠT (10/10) |
| 40 | Cuối kỳ | 4.10 Hướng dẫn cài đặt & Kịch bản demo | Hướng dẫn chi tiết tài khoản mặc định, script seed dữ liệu mẫu | ĐẠT (10/10) |

**KẾT LUẬN ĐỐI CHIẾU:** Đạt **40 / 40 Tiêu chí (100% Hoàn thành)**.
