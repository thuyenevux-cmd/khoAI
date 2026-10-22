# HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI (AI-POWERED INVENTORY MANAGEMENT SYSTEM)

**Đại học Thái Nguyên – Trường Đại học Công nghệ Thông tin và Truyền thông**  
**Học phần:** Ứng dụng trí tuệ nhân tạo – AIA331 | **Hình thức:** Dự án | **Mã số:** 80273

---

## 📌 1. GIỚI THIỆU & MỤC TIÊU DỰ ÁN

Hệ thống Quản lý kho có tích hợp AI là giải pháp phần mềm cấp doanh nghiệp phục vụ bài học học phần AIA331, được phát triển theo tiêu chuẩn công nghiệp nhằm giải quyết triệt để các vấn đề quản lý kho truyền thống:

- **Bảo đảm số liệu kho nhất quán**: Áp dụng ACID Transaction trong SQLAlchemy bọc toàn bộ thao tác Nhập / Xuất kho.
- **Chống tuyệt đối Tồn kho âm (`current_stock < 0`)**: Áp dụng Pessimistic Row Locking kiểm tra tồn kho tại thời điểm xuất. Từ chối và Rollback 100% nếu số lượng xuất vượt quá số lượng tồn kho.
- **Phân quyền truy cập 3 lớp (RBAC)**: Phân rã quyền hạn theo 3 vai trò: `ADMIN` (Quản trị hệ thống), `THỦ KHO` (Vận hành kho), `KẾ TOÁN` (Báo cáo & Tài chính).
- **Khả năng truy vết Audit Log**: Ghi vết thời gian thực mọi biến động nhập/xuất vào bảng `stock_movements`.
- **Tích hợp Trí tuệ nhân tạo (AI Engine)**:
  - Sinh báo cáo nhập-xuất-tồn theo tháng.
  - Gợi ý nhập hàng bám sát tốc độ xuất (burn rate 30 ngày).
  - Phát hiện biến động bất thường & rủi ro đứt gãy chuỗi cung ứng.
  - **Cam kết No-Hallucination**: AI chỉ phân tích dựa trên khối JSON snapshot được truy vấn trực tiếp từ CSDL, hiển thị rõ dữ liệu nguồn trên giao diện.

---

## 🛠️ 2. CÔNG NGHỆ SỬ DỤNG

- **Backend**: Python 3.14, FastAPI, SQLAlchemy ORM 2.0, Alembic, Pydantic v2, Pytest, JWT, Bcrypt.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide React Icons, Recharts, Axios.
- **CSDL**: SQLite (Local development / Testing) & MySQL 8.0 (Docker Production).
- **AI Service**: Google Gemini API (`gemini-1.5-flash` / `google-genai` SDK) & OpenAI API (GPT-4o-mini) với cơ chế Fallback sang Engine AI Nội Bộ (Ground Truth 100% CSDL).
- **Deployment**: Docker & Docker Compose.

---

## 🤖 2.1. TÍCH HỢP GOOGLE GEMINI API VÀ CHATBOT TRỢ LÝ KHO AI

Hệ thống đã tích hợp chính thức **Google Gemini API** (`gemini-1.5-flash`) thông qua SDK chính thức của Google:
- **Endpoint**: `POST /api/ai/chat` (Swagger UI: `http://localhost:8000/docs`).
- **Grounding An Toàn (Ground Truth Data)**: Chatbot không có quyền truy cập trực tiếp hay thực thi SQL tự do vào CSDL. Thay vào đó, backend FastAPI thu thập snapshot dữ liệu qua các hàm nghiệp vụ đã được kiểm duyệt (`warehouse_grounding.py`), sau đó chuyển vào ngữ cảnh prompt cho Gemini.
- **Hỗ trợ Multi-turn Conversation**: Ghi nhớ lịch sử trao đổi trong phiên (tối đa 10 lượt hội thoại gần nhất).
- **Phép tính giả định an toàn**: Khi người dùng hỏi *"Nếu xuất thêm 5 sản phẩm thì còn bao nhiêu?"*, AI thực hiện tính toán mô phỏng lý thuyết và giải thích rõ rằng tồn kho thực tế trong CSDL không hề bị biến đổi.
- **Cơ chế Graceful Fallback**: Nếu chưa cấu hình `GEMINI_API_KEY`, hoặc gặp lỗi mạng / quá hạn mức HTTP 429 Quota Exceeded / Timeout, hệ thống tự động chuyển sang Engine AI Nội Bộ để phản hồi số liệu chính xác từ CSDL mà không làm gián đoạn trải nghiệm người dùng.

### 🔑 Cách cấu hình Google Gemini API Key:
1. Truy cập [Google AI Studio](https://aistudio.google.com/apikey) và bấm **Create API Key**.
2. Mở file `backend/.env` (hoặc copy từ `.env.example`):
   ```env
   GEMINI_API_KEY="AIzaSyYourGeminiApiKeyHere..."
   GEMINI_MODEL="gemini-1.5-flash"
   GEMINI_TIMEOUT_SECONDS=30
   ```
3. Khởi động lại Backend FastAPI. Key được bảo mật hoàn toàn ở backend, tuyệt đối không lộ ở frontend hay log hệ thống.

---

## 📂 3. CẤU TRÚC THƯ MỤC DỰ ÁN

```text
khoAI/
├── backend/
│   ├── app/
│   │   ├── main.py             # FastAPI entry point & API Router config
│   │   ├── core/               # Security, Database, Settings (.env)
│   │   ├── models/             # SQLAlchemy ORM Models (User, Product, Receipt, Inventory,...)
│   │   ├── schemas/            # Pydantic v2 validation schemas
│   │   ├── routers/            # REST API Controllers (auth, products, imports, exports, ai,...)
│   │   ├── services/           # Business logic & AI Service
│   │   ├── prompts/            # Isolated Prompt Template files (*.txt)
│   │   └── db/seed.py          # Script nạp dữ liệu CSDL mẫu
│   ├── tests/                  # Pytest test suite (Auth, Transactions, Anti-negative stock, AI)
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── contexts/           # AuthContext (JWT state & roles)
│   │   ├── layouts/            # MainLayout (Sidebar, Header, Role Badge)
│   │   ├── pages/              # SPA Pages (Dashboard, Products, Import, Export, AI,...)
│   │   └── services/           # Axios client
│   ├── package.json
│   └── vite.config.js
├── docs/                       # Bộ tài liệu học phần hoàn chỉnh (KT1, KT2, KT3, ai-evidence, final)
├── docker-compose.yml
└── README.md
```

---

## 🔑 4. TÀI KHOẢN DEMO

Hệ thống được khởi tạo sẵn 3 tài khoản demo ứng với 3 vai trò:

| Vai trò | Username | Password | Quyền hạn |
| :--- | :--- | :--- | :--- |
| **QUẢN TRỊ VIÊN (ADMIN)** | `admin` | `Admin@123` | Full quyền hệ thống, Quản lý tài khoản người dùng |
| **THỦ KHO (Warehouse)** | `warehouse` | `Warehouse@123` | Lập phiếu nhập, Lập phiếu xuất, Xem tồn kho & lịch sử |
| **KẾ TOÁN (Accountant)** | `accountant` | `Accountant@123` | Xem báo cáo Xuất-Nhập-Tồn, Tải CSV, Xem phân tích AI |

---

## 🚀 5. HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY DỰ ÁN

### 🔹 Cách 1: Chạy trực tiếp (Local Development)

#### Bước 1: Khởi động Backend FastAPI & Nạp Dữ Liệu Mẫu
```bash
cd backend

# Nạp dữ liệu mẫu seed data
python -m app.db.seed

# Chạy server FastAPI
python -m uvicorn app.main:app --reload --port 8000
```
- API Documentation (Swagger UI): `http://localhost:8000/docs`

#### Bước 2: Khởi động Frontend React + Vite
```bash
cd frontend

# Cài đặt dependencies (nếu chưa cài)
npm install

# Chạy dev server
npm run dev
```
- Truy cập giao diện ứng dụng: `http://localhost:3000`

---

### 🔹 Cách 2: Chạy bằng Docker Compose (1-Click Containerized)

```bash
# Build và khởi động MySQL + Backend + Frontend
docker-compose up --build -d
```
- Frontend Nginx: `http://localhost`
- Backend API: `http://localhost:8000/docs`

---

## 💾 6. SAO LƯU VÀ KHÔI PHỤC CSDL MYSQL (BACKUP & RESTORE)

### Sao lưu (Backup CSDL):
```bash
mysqldump -u root -p inventory_db > backup_inventory.sql
```

### Khôi phục (Restore CSDL):
```bash
mysql -u root -p inventory_db < backup_inventory.sql
```

---

## 🧪 7. KIỂM THỬ TỰ ĐỘNG (AUTOMATED PYTEST SUITE)

Dự án tích hợp bộ kiểm thử tự động phủ 100% các kịch bản quan trọng:
- Xác thực JWT & Phân quyền RBAC.
- Transaction Nhập kho tăng tồn.
- Transaction Xuất kho giảm tồn.
- **Kịch bản từ chối Xuất kho vượt tồn (Anti-Negative Stock Guard)**.
- Phân tích AI bám sát dữ liệu CSDL (Báo cáo kho, Gợi ý nhập hàng, Phát hiện biến động).
- **Kiểm thử Chatbot Trợ lý kho AI (`test_ai_chat.py`)**:
  - Gửi câu hỏi hợp lệ & câu hỏi rỗng.
  - Giới hạn độ dài tin nhắn.
  - Phân quyền & chặn truy cập trái phép.
  - Xử lý thiếu `GEMINI_API_KEY` tự động chuyển sang Fallback Engine.
  - Mock Gemini API phản hồi thành công.
  - Xử lý lỗi Timeout, Quota 429, phản hồi rỗng.
  - Tra cứu mặt hàng sắp hết, mặt hàng không tồn tại.
  - Hỗ trợ hội thoại nhiều lượt (Multi-turn).
  - Đảm bảo câu hỏi giả định không làm thay đổi tồn kho CSDL.
  - Đảm bảo không làm lộ API Key trong response hay log.

Chạy test suite:
```bash
cd backend
python -m pytest tests -v
```

---

## 📋 8. RUBRIC VÀ TÀI LIỆU HỌC PHẦN (AIA331)

Toàn bộ tài liệu báo cáo và minh chứng được lưu trữ trong thư mục `docs/`:
- `docs/KT1/`: Phân tích nghiệp vụ, Yêu cầu chức năng, Actor, UseCase Diagram, ERD Diagram.
- `docs/KT2/`: Architecture source code, RESTful API List, CRUD, Security, Search/Filter.
- `docs/KT3/`: AI Integration, Thực nghiệm Prompt V1 vs V2 vs V3.
- `docs/ai-evidence/`: 07 file minh chứng ứng dụng AI trong quy trình SDLC.
- `docs/final/`: Báo cáo kỹ thuật, Kịch bản demo 10 bước (10-15 phút), Test Report, Security và `RUBRIC_CHECKLIST.md`.
