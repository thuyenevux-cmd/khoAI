# RUBRIC CHECKLIST ĐÁNH GIÁ MÔN HỌC (AIA331)

**Đại học Thái Nguyên – Trường Đại học Công nghệ Thông tin và Truyền thông**  
**Học phần:** Ứng dụng trí tuệ nhân tạo – AIA331 | **Mã số:** 80273  
**Dự án:** Hệ thống quản lý kho có tích hợp AI (AI-Powered Inventory Management System)

---

## 📋 I. BẢNG ĐÁNH GIÁ TIÊU CHÍ BÀI KIỂM TRA 1 (KT1)

| STT | Tiêu chí KT1 | Trạng thái | File minh chứng | Ghi chú |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Phân tích bài toán quản lý kho | ✅ Đã hoàn thành | `docs/KT1/01_Phan_tich_bai_toan.md` | Phân tích thực trạng và giải pháp |
| 2 | Yêu cầu chức năng (Functional) | ✅ Đã hoàn thành | `docs/KT1/02_Yeu_cau_chuc_nang.md` | Đủ 18 yêu cầu FR |
| 3 | Yêu cầu phi chức năng (Non-Functional) | ✅ Đã hoàn thành | `docs/KT1/03_Yeu_cau_phi_chuc_nang.md` | Bảo mật JWT, Performance |
| 4 | Phân tích Actor & UseCase | ✅ Đã hoàn thành | `docs/KT1/04_Actor_UseCase.md` | Sơ đồ Mermaid UseCase chuẩn |
| 5 | Thiết kế CSDL (ERD Diagram) | ✅ Đã hoàn thành | `docs/KT1/05_ERD.md` | Sơ đồ Mermaid ERD 11 bảng |
| 6 | Kiến trúc hệ thống 3-Tier | ✅ Đã hoàn thành | `docs/KT1/06_Kien_truc.md` | FastAPI + React + SQLAlchemy |
| 7 | Vị trí và vai trò của AI | ✅ Đã hoàn thành | `docs/KT1/07_Vi_tri_AI.md` | Tích hợp trực tiếp nghiệp vụ |
| 8 | Thiết kế Prompt AI | ✅ Đã hoàn thành | `docs/KT1/08_Prompt_AI.md` | Mẫu System & User Prompts |
| 9 | Minh chứng ứng dụng AI SDLC | ✅ Đã hoàn thành | `docs/KT1/09_Minh_chung_AI.md` | Quy trình SDLC tích hợp AI |
| 10| Kế hoạch phát triển chi tiết | ✅ Đã hoàn thành | `docs/KT1/10_Ke_hoach.md` | Lộ trình 15 Phases khép kín |

---

## 📋 II. BẢNG ĐÁNH GIÁ TIÊU CHÍ BÀI KIỂM TRA 2 (KT2)

| STT | Tiêu chí KT2 | Trạng thái | File minh chứng | Ghi chú |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Kiến trúc Source Code | ✅ Đã hoàn thành | `docs/KT2/01_Kien_truc_source_code.md` | Phân rã Layered Clean Architecture |
| 2 | Danh sách RESTful APIs | ✅ Đã hoàn thành | `docs/KT2/02_Danh_sach_API.md` | Đủ REST APIsSwagger `/docs` |
| 3 | Chức năng CRUD cơ bản | ✅ Đã hoàn thành | `backend/app/routers/` | Products, Categories, Units, Suppliers |
| 4 | Authentication & RBAC | ✅ Đã hoàn thành | `backend/app/routers/auth.py` | JWT + 3 Roles (ADMIN, WH, ACC) |
| 5 | Search & Filter | ✅ Đã hoàn thành | `frontend/src/pages/` | Tìm kiếm & lọc đa tiêu chí |
| 6 | Dashboard Thống kê | ✅ Đã hoàn thành | `frontend/src/pages/DashboardPage.jsx` | KPI Cards & Recharts |
| 7 | Error Handling chuẩn hoá | ✅ Đã hoàn thành | `backend/app/main.py` | Response JSON lỗi đồng nhất |
| 8 | Seed Data khởi tạo CSDL | ✅ Đã hoàn thành | `backend/app/db/seed.py` | Nạp dữ liệu mẫu tự động |
| 9 | Hướng dẫn README | ✅ Đã hoàn thành | `README.md` | Hướng dẫn chạy local & Docker |
| 10| Minh chứng AI Coding | ✅ Đã hoàn thành | `docs/ai-evidence/` | 07 file minh chứng SDLC |

---

## 📋 III. BẢNG ĐÁNH GIÁ TIÊU CHÍ BÀI KIỂM TRA 3 (KT3)

| STT | Tiêu chí KT3 | Trạng thái | File minh chứng | Ghi chú |
| :---: | :--- | :---: | :--- | :--- |
| 1 | Tích hợp AI Service | ✅ Đã hoàn thành | `backend/app/services/ai_service.py` | Decoupled Interface + Fallback Engine |
| 2 | Thực nghiệm Prompt V1/V2/V3 | ✅ Đã hoàn thành | `docs/KT3/02_Prompt_Experiment.md` | So sánh chi tiết 3 phiên bản |
| 3 | Tách biệt Prompt Template | ✅ Đã hoàn thành | `backend/app/prompts/*.txt` | File text riêng biệt trong repository |
| 4 | Chống AI Hallucination | ✅ Đã hoàn thành | `backend/app/routers/ai.py` | Chỉ nhận JSON truy vấn từ CSDL |
| 5 | Minh bạch nguồn dữ liệu | ✅ Đã hoàn thành | `frontend/src/pages/AIAnalysisPage.jsx` | Hiển thị khoang JSON Snapshot |
| 6 | Xử lý lỗi AI Resilience | ✅ Đã hoàn thành | `backend/app/services/ai_service.py` | Chuyển đổi mềm dẻo khi lỗi API Key |
| 7 | AI Feature 1 - Báo cáo Kho | ✅ Đã hoàn thành | `POST /api/ai/inventory-report` | Sinh báo cáo Markdown 4 mục |
| 8 | AI Feature 2 - Gợi ý Nhập | ✅ Đã hoàn thành | `POST /api/ai/restock-recommendation`| Phân cấp ưu tiên bám burn rate |
| 9 | AI Feature 3 - Bất thường | ✅ Đã hoàn thành | `POST /api/ai/anomaly-summary` | Nhận diện đứt gãy cung ứng |
| 10| Test Suite cho AI Endpoints | ✅ Đã hoàn thành | `backend/tests/test_ai.py` | Pytest PASSED 100% |

---

## 📋 IV. BẢNG ĐÁNH GIÁ TIÊU CHÍ BÀI THI CUỐI KỲ (FINAL EVALUATION)

| STT | Tiêu chí Cuối Kỳ | Trạng thái | File minh chứng | Ghi chú |
| :---: | :--- | :---: | :--- | :--- |
| 1 | DB Transaction Nhập/Xuất Kho | ✅ Đã hoàn thành | `backend/app/routers/imports.py` & `exports.py` | Atomic Transaction ACID |
| 2 | Chống tuyệt đối Tồn Kho Âm | ✅ Đã hoàn thành | `backend/app/routers/exports.py` | Lock dòng + Refuse overflow qty |
| 3 | Phân quyền 3 vai trò (RBAC) | ✅ Đã hoàn thành | `backend/app/routers/deps.py` | ADMIN, THỦ KHO, KẾ TOÁN |
| 4 | Audit Trail Truy vết | ✅ Đã hoàn thành | `backend/app/models/stock_movement.py` | Bảng stock_movements |
| 5 | Giao diện Frontend Chuyên nghiệp| ✅ Đã hoàn thành | `frontend/src/` | React + Vite + Tailwind CSS |
| 6 | Đóng gói Docker Compose | ✅ Đã hoàn thành | `docker-compose.yml` | MySQL + FastAPI + Vite Nginx |
| 7 | Kịch bản Demo 10 Bước | ✅ Đã hoàn thành | `docs/final/02_Huong_dan_demo.md` | Chi tiết 10-15 phút demo |
| 8 | Kiểm thử Tự động Pytest | ✅ Đã hoàn thành | `backend/tests/` | **11/11 PASSED (100%)** |
| 9 | Bộ tài liệu học phần AIA331 | ✅ Đã hoàn thành | `docs/` | Đủ tất cả file bài nộp |
| 10| Khả năng Demo trực tiếp | ✅ Đã hoàn thành | `python -m app.db.seed` | Chạy sẵn sàng 1-click |
