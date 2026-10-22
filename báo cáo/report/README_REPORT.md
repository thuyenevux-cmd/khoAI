# BỘ HỒ SƠ BÁO CÁO KỸ THUẬT ĐỒ ÁN HỌC PHẦN AIA331
## HỆ THỐNG QUẢN LÝ KHO CÓ TÍCH HỢP AI (AI-POWERED INVENTORY MANAGEMENT SYSTEM)

**Cơ sở đào tạo:** Trường Đại học Công nghệ Thông tin và Truyền thông - Đại học Thái Nguyên  
**Học phần:** Ứng dụng trí tuệ nhân tạo (AIA331) | **Mã số:** 80273  
**Giảng viên hướng dẫn:** ThS. NGUYỄN TUẤN ANH  
**Sinh viên thực hiện:**  
1. **Dương Minh Quang** - Mã sinh viên: `DTC245200225`  
2. **Vũ Ngọc Anh Thuyên** - Mã sinh viên: `DTC245200428`  
**Lớp:** Công nghệ Thông tin - K24 ICTU  
**Năm hoàn thành:** 2026  

---

## 1. CẤU TRÚC THƯ MỤC HỒ SƠ BÁO CÁO

```text
D:\it-thesis-research-documentation-engineer-v3.0\report\
├── Word\
│   ├── Bao_cao_AIA331.docx       <- Tệp Word hoàn chỉnh chuẩn form ICTU (16 chương + phụ lục)
│   └── Bao_cao_AIA331.pdf        <- Bản in PDF chuẩn chỉ xuất trực tiếp qua Word COM
├── LaTeX\
│   ├── main.tex                  <- Tệp điều phối chính
│   ├── ictu_style.sty            <- Gói style định dạng chuẩn ICTU (Times New Roman, lề chuẩn)
│   ├── ddl.sql                   <- Toàn văn mã khởi tạo CSDL 11 bảng chuẩn 3NF
│   ├── chapters/                 <- 16 chương nội dung + bìa + rubric + mở đầu + phụ lục
│   │   ├── cover.tex             <- Trang bìa khung đôi TikZ chuẩn nhận diện ICTU
│   │   ├── rubric_evaluation.tex <- Phiếu đánh giá 40 tiêu chí của Giảng viên hướng dẫn
│   │   ├── ch01_tong_quan.tex ... ch16_ket_luan.tex
│   │   └── appendix.tex          <- Phụ lục ma trận truy vết và DDL
│   └── figures/                  <- 11 sơ đồ kỹ thuật + 5 ảnh chụp giao diện + logo ICTU
├── DrawIO/                       <- 11 tệp sơ đồ kỹ thuật định dạng XML mở rộng (.drawio)
│   ├── usecase.drawio            <- Sơ đồ Use Case tổng thể (4 Actors)
│   ├── erd.drawio                <- Sơ đồ thực thể liên kết ERD 11 bảng
│   ├── architecture.drawio       <- Kiến trúc 3-Tier Client-Server
│   ├── activity_login.drawio     <- Sơ đồ hoạt động Đăng nhập & RBAC
│   ├── activity_import.drawio    <- Sơ đồ hoạt động Nhập kho
│   ├── activity_export.drawio    <- Sơ đồ hoạt động Xuất kho chống âm
│   ├── ai_flow.drawio            <- Sơ đồ hoạt động Xử lý AI & Cảnh báo
│   ├── data_flow.drawio          <- Sơ đồ luồng dữ liệu DFD Mức 0 và 1
│   ├── sequence_import.drawio    <- Sơ đồ tuần tự Nhập kho
│   ├── sequence_export.drawio    <- Sơ đồ tuần tự Xuất kho
│   └── sequence_ai_report.drawio <- Sơ đồ tuần tự Hỏi đáp Trợ lý AI
├── Images/                       <- 11 ảnh sơ đồ xuất độ phân giải cao (PNG) + logo_ictu.png
├── Screenshots/                  <- 5 ảnh chụp giao diện thực tế hệ thống
│   ├── screenshot_login.png      <- Giao diện Đăng nhập JWT OAuth2
│   ├── screenshot_dashboard.png  <- Giao diện Bảng điều khiển KPI Dashboard
│   ├── screenshot_ai_report.png  <- Giao diện AI Analytics Hub
│   ├── screenshot_ai_assistant.png <- Giao diện Trợ lý hỏi đáp tự nhiên NLP
│   └── screenshot_products.png   <- Giao diện Quản lý danh mục Sản phẩm
└── ddl.sql                       <- Script DDL SQL khởi tạo 11 bảng CSDL 3NF
```

---

## 2. KẾT QUẢ THỰC NGHIỆM ĐỊNH LƯỢNG (GROUND-TRUTH)

- **Kiểm thử tự động:** 12/12 ca kiểm thử (Test Cases) đạt trạng thái **PASSED (100%)** với thời gian chạy **4.07 giây** trên framework `pytest`.
- **An toàn giao dịch:** Cơ chế Transaction Rollback bảo đảm **không bao giờ xảy ra âm tồn kho** khi số lượng xuất vượt quá tồn kho thực tế.
- **An toàn tính toán AI:** Khắc phục triệt để ngoại lệ chia cho 0 (`ZeroDivisionError`) khi tốc độ xuất bán `burn_rate == 0`.
- **Hiệu năng hệ thống:**
  - Độ trễ các API thông thường: **15ms - 65ms** (Mục tiêu: <100ms).
  - Độ trễ dịch vụ phân tích AI nội bộ: **350ms - 850ms** (Mục tiêu: <1.5s).

---

## 3. HƯỚNG DẪN TÁI LẬP HỆ THỐNG VÀ KIỂM THỬ

### 3.1. Chạy kiểm thử tự động Backend (Pytest)
```bash
cd "D:\khoAI\thực hành\backend"
python -m pytest
```
*Kết quả:* 12 passed, 15 warnings in 4.07s.

### 3.2. Khởi chạy máy chủ Backend
```bash
cd "D:\khoAI\thực hành\backend"
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
*Tài liệu API Swagger UI:* Truy cập `http://localhost:8000/docs`

### 3.3. Khởi chạy ứng dụng Frontend
```bash
cd "D:\khoAI\thực hành\frontend"
npm run dev
```
*Giao diện Web:* Truy cập `http://localhost:3000` hoặc `http://localhost:5173`
