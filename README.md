# HỆ THỐNG QUẢN LÝ KHO TÍCH HỢP AI (SMART WAREHOUSE AI ASSISTANT)

**Đại học Thái Nguyên – Trường Đại học Công nghệ Thông tin và Truyền thông (ICTU)**  
**Học phần:** Ứng dụng trí tuệ nhân tạo (AIA331) | **Mã học phần:** 80273 | **Nhóm:** 11  

---

## 📌 1. TỔNG QUAN DỰ ÁN

Dự án xây dựng giải pháp phần mềm quản lý kho chuyên nghiệp kết hợp trí tuệ nhân tạo:
- **Backend**: Python 3.12/3.14, FastAPI REST API, SQLAlchemy ORM, SQLite/MySQL, Pydantic v2, Pytest, JWT Authentication.
- **Frontend**: React 18, Vite, Tailwind CSS, Lucide Icons, Axios.
- **Tích hợp AI**: Google Gemini API (`gemini-1.5-flash` / SDK `google-genai`), tự động sinh báo cáo nhập xuất tồn, phát hiện biến động bất thường, gợi ý nhập hàng và **Chatbot Trợ Lý Kho AI** tra cứu trực tiếp theo thời gian thực (Ground Truth - No Hallucination).
- **Kiểm soát tính toàn vẹn (ACID)**: Chống tuyệt đối tồn kho âm (`current_stock < 0`) bằng Pessimistic Locking.

---

## 📂 2. CẤU TRÚC REPOSITORY

* [thực hành/](thực%20hành/): Toàn bộ mã nguồn chạy thực tế của hệ thống.
  * [thực hành/backend/](thực%20hành/backend/): Backend FastAPI, Database models, Grounding logic, Gemini Service, Pytest suite.
  * [thực hành/frontend/](thực%20hành/frontend/): Frontend React SPA với giao diện Dark Mode, Trung tâm phân tích AI & Chatbot Trợ lý kho.
  * [thực hành/docs/](thực%20hành/docs/): Tài liệu hướng dẫn chi tiết ([GEMINI_CHATBOT_GUIDE.md](thực%20hành/docs/GEMINI_CHATBOT_GUIDE.md)), báo cáo KT1, KT2, KT3.
  * [thực hành/docker-compose.yml](thực%20hành/docker-compose.yml): Cấu hình chạy trọn gói containerized.
* [báo cáo/](báo%20cáo/): Hồ sơ báo cáo đồ án hoàn chỉnh.
  * `báo cáo dự án Kho AI nhóm 11.docx`: File báo cáo Microsoft Word chính thức.
  * `báo cáo dự án Kho AI nhóm 11.pdf`: Bản in PDF chất lượng cao.
  * [báo cáo/latex/](báo%20cáo/latex/): Mã nguồn LaTeX hoàn chỉnh.
  * [báo cáo/diagrams/](báo%20cáo/diagrams/): Bộ sơ đồ chuẩn mực V7.0 Pro (ERD 11 bảng CSDL 3NF, Kiến trúc, Usecase, Pipeline AI Fallback...).

---

## 🚀 3. HƯỚNG DẪN KHỞI CHẠY NHANH DÀNH CHO THÀNH VIÊN DỰ ÁN

### Bước 1: Clone Repository
```bash
git clone https://github.com/thuyenevux-cmd/khoAI.git
cd khoAI
```

### Bước 2: Khởi động Backend (FastAPI)
```bash
cd "thực hành/backend"

# 1. Tạo và kích hoạt môi trường ảo Python
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# 2. Cài đặt các thư viện cần thiết
pip install -r requirements.txt

# 3. Tạo file cấu hình .env (copy từ .env.example)
cp .env.example .env
# Điền GEMINI_API_KEY nếu có (hoặc để trống, hệ thống sẽ tự động dùng Fallback Engine nội bộ)

# 4. Nạp dữ liệu mẫu ban đầu
python -m app.db.seed

# 5. Khởi chạy Backend Server
python -m uvicorn app.main:app --reload --port 8000
```
- Swagger API Docs: `http://localhost:8000/docs`

### Bước 3: Khởi động Frontend (React)
```bash
cd "thực hành/frontend"

# Cài đặt thư viện Node
npm install

# Khởi chạy giao diện
npm run dev
```
- Truy cập trình duyệt: `http://localhost:3000`
- Tài khoản đăng nhập demo:
  - **Admin**: `admin` / `Admin@123`
  - **Thủ kho**: `warehouse` / `Warehouse@123`
  - **Kế toán**: `accountant` / `Accountant@123`

---

## 🧪 4. CHẠY KIỂM THỬ TỰ ĐỘNG (AUTOMATED TEST SUITE)

```bash
cd "thực hành/backend"
python -m pytest tests -v
```
Toàn bộ 26/26 ca kiểm thử tự động (Auth, Transaction, Chống âm kho, AI Chatbot) đạt tỷ lệ **Passed 100%**.
