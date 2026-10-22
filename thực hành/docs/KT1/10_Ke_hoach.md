# 10. KẾ HOẠCH TRIỂN KHAI CHI TIẾT (DEVELOPMENT ROADMAP)

---

## 1. LỘ TRÌNH 15 PHASES KHÉP KÍN

| Phase | Nội dung công việc | Đầu ra mong đợi | Trạng thái |
| :---: | :--- | :--- | :---: |
| **Phase 1** | Phân tích & thiết kế kiến trúc | 10 file Markdown trong `docs/KT1/` | ✅ Hoàn thành |
| **Phase 2** | Khởi tạo Backend + Database Models + Seed | Structure `backend/`, Alembic, Seed Data | 🔄 Đang triển khai |
| **Phase 3** | Authentication (JWT) & Phân quyền RBAC | `/api/auth/login`, Middleware roles | ⏳ Chờ |
| **Phase 4** | Core CRUD Danh mục | Products, Categories, Units, Suppliers APIs | ⏳ Chờ |
| **Phase 5** | Transaction Nhập Kho | `/api/imports` + Atomic Stock Increase | ⏳ Chờ |
| **Phase 6** | Transaction Xuất Kho & Anti-Negative Stock | `/api/exports` + Row Lock + Refuse Overflow | ⏳ Chờ |
| **Phase 7** | Theo dõi Tồn Kho & Stock Movements History | `/api/inventory`, `/api/stock-movements` | ⏳ Chờ |
| **Phase 8** | Dashboard APIs & Aggregated Reports | `/api/dashboard`, Export CSV | ⏳ Chờ |
| **Phase 9** | Giao diện Frontend React + Vite + Tailwind | React App, SPA Router, Modals, Charts | ⏳ Chờ |
| **Phase 10**| Integration AI Service | `/api/ai/*` APIs, Prompt files, Provenance | ⏳ Chờ |
| **Phase 11**| Prompt Experiments & KT3 Docs | Prompt V1 vs V2 vs V3 comparison in `docs/KT3/`| ⏳ Chờ |
| **Phase 12**| Automated Pytest Suite | Pytest test suite for DB, Transaction, RBAC | ⏳ Chờ |
| **Phase 13**| Docker Deployment | `docker-compose.yml`, Dockerfiles | ⏳ Chờ |
| **Phase 14**| Complete Academic Docs Suites | Full `docs/KT2/`, `docs/KT3/`, `docs/final/` | ⏳ Chờ |
| **Phase 15**| Final Rubric Audit | `RUBRIC_CHECKLIST.md` 100% compliance | ⏳ Chờ |

---

## 2. QUY TRÌNH KIỂM TRA SAU MỖI PHASE

Sau khi hoàn thành mỗi Phase, hệ thống được chạy kiểm tra thông qua:
1. Chạy thử nghiệm các Endpoint bằng curl/pytest.
2. Kiểm tra log hiển thị dữ liệu và ngoại lệ.
3. Xác minh tính đúng đắn của dữ liệu trong CSDL.
4. Cập nhật tiến độ vào tài liệu dự án.
