# 09. MINH CHỨNG ỨNG DỤNG AI TRONG QUY TRÌNH SDLC (KT1)

---

## 1. KHÁI QUÁT VỀ VIỆC ỨNG DỤNG AI TRONG PHÁT TRIỂN DỰ ÁN

Trong suốt vòng đời phát triển phần mềm (SDLC) cho đề tài này, Trí tuệ nhân tạo (AI Assistant) được áp dụng một cách thực chất và minh bạch qua các công đoạn:

1. **Giai đoạn Phân tích & Thiết kế Kiến trúc (KT1)**:
   - Sử dụng AI hỗ trợ phân tích luồng nghiệp vụ kho, chuẩn hóa ERD 11 bảng và thiết kế Use Case Diagram.
   - AI hỗ trợ sinh cấu trúc các file Markdown định dạng chuẩn cho bài thi.
2. **Giai đoạn Xây dựng Backend & Frontend (KT2)**:
   - Sử dụng AI sinh boilerplate code cho FastAPI, Pydantic schemas, SQLAlchemy models.
   - AI hỗ trợ viết thuật toán Pessimistic Locking `with_for_update()` chống tồn âm trong DB Transaction.
3. **Giai đoạn Tích hợp AI & Prompt Engineering (KT3)**:
   - AI hỗ trợ tối ưu hóa 3 phiên bản Prompt (V1, V2, V3) ngăn chặn Hallucination.
   - AI sinh bộ dữ liệu seed và test case với Pytest.
4. **Giai đoạn Đóng gói & Báo cáo Final**:
   - AI hỗ trợ viết script `docker-compose.yml`, README.md và kịch bản demo 10 bước.

---

## 2. CẤU TRÚC LƯU TRỮ CÁC MINH CHỨNG THEO QUY ĐỊNH

Các minh chứng chi tiết được lưu trữ tại thư mục `docs/ai-evidence/` gồm 7 file:
- `01_phan_tich_nghiep_vu.md`: Prompt & Kết quả phân tích quy trình kho.
- `02_thiet_ke_erd.md`: Prompt & Kết quả sinh sơ đồ ERD Mermaid.
- `03_sinh_api.md`: Prompt & Code sinh FastAPI router + schemas.
- `04_transaction.md`: Prompt & Code xử lý Transaction khóa dòng chống tồn âm.
- `05_ai_prompt.md`: Prompt & Thử nghiệm thiết kế System Prompt cho AI.
- `06_test_case.md`: Prompt & Code sinh bộ Pytest suite.
- `07_code_review.md`: Prompt & Đánh giá an toàn bảo mật JWT / SQL Injection.
