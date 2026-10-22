# HƯỚNG DẪN TÍCH HỢP GOOGLE GEMINI API VÀ SỬ DỤNG CHATBOT TRỢ LÝ KHO AI

**Dự án học phần:** Ứng dụng trí tuệ nhân tạo – AIA331 | **Mã số:** 80273  
**Hệ thống quản lý kho thông minh tích hợp AI (SaaS Edition)**

---

## 📌 1. TỔNG QUAN CHỨC NĂNG CHATBOT TRỢ LÝ KHO AI

Chức năng **Chatbot Trợ Lý Kho AI** được tích hợp trực tiếp vào mục **AI** của hệ thống (Tab 4: *Chatbot Trợ Lý Kho AI*), hỗ trợ:
1. **Giải đáp nghiệp vụ kho**: Hướng dẫn quy trình tạo phiếu nhập kho, phiếu xuất kho, nguyên nhân hệ thống từ chối xuất kho (ví dụ: không đủ số lượng tồn khả dụng).
2. **Truy vấn số liệu tồn kho theo thời gian thực (Ground Truth)**: Tra cứu nhanh số lượng tồn, đơn vị tính, đơn giá nhập gần nhất, tốc độ xuất 30 ngày (burn rate) và ước tính số ngày còn đủ hàng.
3. **Cảnh báo thiếu hàng & Đề xuất nhập kho**: Liệt kê các sản phẩm có tồn kho dưới mức tối thiểu hoặc đã hết hàng.
4. **Hội thoại đa lượt (Multi-turn Conversation)**: Ghi nhớ ngữ cảnh đối thoại trong phiên, hỗ trợ hỏi tiếp (ví dụ: *"Mã HH001 còn bao nhiêu hàng?"* -> *"Nếu xuất thêm 3 cái thì còn bao nhiêu?"*).
5. **Tính toán giả định an toàn**: Thực hiện tính toán mô phỏng mà tuyệt đối **không làm thay đổi số liệu CSDL**.
6. **Cơ chế Fallback thông minh**: Tự động chuyển đổi sang Engine AI Nội Bộ khi chưa có API Key, gặp lỗi mạng, quá hạn mức Quota HTTP 429 hoặc Timeout.

---

## 🔑 2. HƯỚNG DẪN LẤY VÀ CẤU HÌNH GEMINI API KEY

### Bước 1: Lấy API Key từ Google AI Studio
1. Truy cập đường dẫn chính thức: [https://aistudio.google.com/apikey](https://aistudio.google.com/apikey).
2. Đăng nhập bằng tài khoản Google.
3. Bấm **Create API Key** (Tạo khóa API) -> Chọn Project của bạn hoặc tạo mới.
4. Sao chép chuỗi API Key được cấp.

### Bước 2: Cấu hình vào file `.env` của Backend
Mở file `backend/.env` (tạo từ `backend/.env.example` nếu chưa có) và điền key:
```env
PROJECT_NAME="AI-Powered Inventory Management System"
API_V1_STR="/api"
SECRET_KEY="ai_inventory_secret_key_change_in_production_2026"
ACCESS_TOKEN_EXPIRE_MINUTES=1440
DATABASE_URL="sqlite:///./inventory.db"

# Google Gemini API Settings (Official)
GEMINI_API_KEY="AIzaSyYourActualApiKeyHere..."
GEMINI_MODEL="gemini-1.5-flash"
GEMINI_TIMEOUT_SECONDS=30
```

> [!IMPORTANT]
> **Nguyên tắc bảo mật:**
> - API Key chỉ được lưu trữ và đọc tại backend FastAPI (`backend/.env`).
> - File `.env` đã được đưa vào `.gitignore`, tuyệt đối không commit lên Git repository.
> - API Key không bao giờ được gửi về frontend hoặc hiển thị trong log hệ thống.

---

## 📦 3. CÀI ĐẶT THƯ VIỆN VÀ KHỞI CHẠY HỆ THỐNG

### Bước 1: Cài đặt thư viện Backend
Thư viện chính thức `google-genai` đã được khai báo trong `requirements.txt`:
```bash
cd backend
python -m venv venv
# Kích hoạt venv (Windows):
.\venv\Scripts\activate
# Cài đặt toàn bộ thư viện:
pip install -r requirements.txt
```

### Bước 2: Khởi động Backend FastAPI
```bash
cd backend
# Nạp dữ liệu mẫu ban đầu (nếu là lần đầu khởi tạo):
python -m app.db.seed

# Khởi chạy server API cổng 8000:
python -m uvicorn app.main:app --reload --port 8000
```
- API Docs (Swagger UI): `http://localhost:8000/docs`

### Bước 3: Khởi động Frontend React
```bash
cd frontend
# Cài đặt dependencies (lần đầu):
npm install

# Khởi chạy dev server:
npm run dev
```
- Giao diện người dùng: `http://localhost:3000` (hoặc cổng được hiển thị trong terminal).

---

## 🔍 4. KIỂM TRA API TRÊN SWAGGER UI

1. Mở trình duyệt truy cập: `http://localhost:8000/docs`.
2. Đăng nhập lấy Bearer Token qua endpoint `POST /api/auth/login`:
   - `username`: `admin`
   - `password`: `Admin@123`
3. Nhấp nút **Authorize** ở góc trên bên phải Swagger và dán `access_token`.
4. Tìm đến endpoint **`POST /api/ai/chat`**:
   - Gửi payload mẫu:
     ```json
     {
       "message": "Sản phẩm nào đang dưới mức tồn tối thiểu?",
       "conversation_id": "test_conv_01",
       "history": []
     }
     ```
   - Nhận phản hồi chuẩn:
     ```json
     {
       "success": true,
       "conversation_id": "test_conv_01",
       "reply": "### ⚠️ Danh Sách Mặt Hàng Cần Chú Ý...",
       "sources": [
         {"type": "low_stock_summary", "count": 2}
       ],
       "provider": "Google Gemini API (gemini-1.5-flash)",
       "error": null,
       "timestamp": "2026-10-22 23:30:00"
     }
     ```

---

## 🛡️ 5. XỬ LÝ CÁC TÌNH HUỐNG NGOẠI LỆ & LỖI HẠN MỨC

| Tình huống | Hành vi hệ thống | Thông báo hiển thị |
| :--- | :--- | :--- |
| **Chưa cấu hình API Key** | Tự động chuyển sang Engine AI Nội Bộ, đọc trực tiếp snapshot CSDL | Kèm thông báo: *Hệ thống đang chạy ở chế độ Engine AI Nội Bộ do chưa cấu hình GEMINI_API_KEY.* |
| **HTTP 429 Quota Exceeded** | Bắt ngoại lệ 429, tự động chuyển sang Fallback Engine để không làm đứt quãng trải nghiệm | Cảnh báo: *Google Gemini API đã chạm giới hạn hạn mức (Rate Limit/Quota Exceeded).* |
| **Gemini API Timeout (>30s)** | Bắt lỗi Timeout, tự động chuyển sang Engine AI Nội Bộ | Cảnh báo: *Yêu cầu bị quá thời gian (Timeout). Hệ thống tự động sử dụng Engine AI Nội Bộ.* |
| **Câu hỏi rỗng hoặc khoảng trắng** | Chặn ở tầng Pydantic Schema Validation | Trả về mã lỗi HTTP 422: *Câu hỏi không được để trống.* |
| **Câu hỏi quá dài (>1000 ký tự)** | Giới hạn độ dài để bảo vệ token và chống tràn buffer | Trả về mã lỗi HTTP 422. |
| **Không có quyền truy cập** | Chặn qua dependency `require_roles` | Trả về mã lỗi HTTP 401 Unauthorized / 403 Forbidden. |

---

## 🧪 6. CHẠY BỘ KIỂM THỬ TỰ ĐỘNG (PYTEST)

Hệ thống có bộ test suite hoàn chỉnh trong `tests/test_ai_chat.py` gồm 14 ca kiểm thử chuyên sâu:
```bash
cd backend
$env:PYTHONPATH="."
python -m pytest tests/test_ai_chat.py -v
```

Kết quả: **14/14 tests PASSED 100%**.

---

## ⚠️ 7. NHỮNG GIỚI HẠN HIỆN TẠI VÀ KHUYẾN NGHỊ VẬN HÀNH

1. **Phân định rõ tư vấn và giao dịch**: Chatbot là công cụ tra cứu, tư vấn thông minh; chatbot **không tự động ký duyệt hoặc thay đổi trực tiếp tồn kho** mà hướng dẫn người dùng thao tác qua màn hình *Nhập kho* / *Xuất kho*.
2. **Hạn mức Google AI Studio Free Tier**: Tài khoản dùng gói miễn phí của Google AI Studio có thể bị giới hạn số lượng request trên phút (RPM/RPD). Khi vượt ngưỡng, hệ thống sẽ kích hoạt Fallback Engine. Khuyến nghị nâng cấp Billing Pay-as-you-go trên Google Cloud nếu sử dụng thương mại quy mô lớn.
3. **Độ tươi mới của dữ liệu**: Mọi câu hỏi đều được backend tạo snapshot thời gian thực ngay khi nhận được request, đảm bảo số liệu chính xác từng giây.
