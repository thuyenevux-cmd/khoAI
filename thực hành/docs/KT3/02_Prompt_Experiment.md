# KT3 - 02. THỰC NGHIỆM TỐI ƯU HÓA PROMPT AI (PROMPT EXPERIMENTS)

**Học phần:** Ứng dụng trí tuệ nhân tạo – AIA331

---

## 1. MỤC TIÊU THỰC NGHIỆM

So sánh 3 phiên bản Prompt (V1, V2, V3) nhằm đánh giá khả năng bám sát số liệu CSDL thực tế, khả năng phát hiện điểm bất thường và triệt tiêu hiện tượng AI Hallucination (tự bịa số liệu/sản phẩm không có).

---

## 2. BẢNG SO SÁNH NỘI DUNG 3 PHIÊN BẢN PROMPT

### 🔴 Prompt V1 (Phiên bản Cơ bản / Sơ khởi)
- **Nội dung System Prompt**: *"Bạn là trợ lý quản lý kho. Hãy phân tích dữ liệu kho và viết báo cáo."*
- **Đánh giá kết quả**:
  - **Độ chính xác**: 60%. Có xu hướng suy đoán các sản phẩm phổ biến như "Chuột máy tính" mặc dù JSON đầu vào không có.
  - **Độ ngắn gọn**: Lan man.
  - **Khả năng bám số liệu**: Kém. AI tự đưa ra con số đề xuất nhập hàng 50 cái mà không có công thức.
  - **Hiện tượng Hallucination**: Có xảy ra.

---

### 🟡 Prompt V2 (Phiên bản Bổ sung Quy tắc)
- **Nội dung System Prompt**: *"Bạn là trợ lý kho. Phân tích dữ liệu JSON được cấp. Không tự tạo số liệu mới. Hãy liệt kê hàng dưới tồn tối thiểu và đưa ra gợi ý nhập hàng."*
- **Đánh giá kết quả**:
  - **Độ chính xác**: 85%. Đã hạn chế được việc bịa tên sản phẩm mới.
  - **Độ ngắn gọn**: Khá tốt.
  - **Khả năng bám số liệu**: Khá. Đã trích dẫn được số liệu tồn kho hiện tại.
  - **Hiện tượng Hallucination**: Thỉnh thoảng vẫn đưa ra nhận xét nguyên nhân bên ngoài (ví dụ: "do thị trường tiêu thụ mạnh").

---

### 🟢 Prompt V3 (Phiên bản Khắt khe - Được Chọn Triển Khai)
- **Nội dung System Prompt**:
  ```text
  Bạn là trợ lý quản lý kho doanh nghiệp.
  Nhiệm vụ: Phân tích dữ liệu kho được cung cấp và tạo báo cáo ngắn gọn, chính xác, dễ hiểu.

  QUY TẮC BẮT BUỘC:
  1. Chỉ sử dụng số liệu được cung cấp trong JSON đầu vào.
  2. Tuyệt đối không tự tạo số liệu mới hoặc bịa ra tên sản phẩm không có.
  3. Không suy đoán dữ liệu không có trong đầu vào. Nếu dữ liệu không đủ, phải nói rõ.
  4. Không thay đổi số liệu đầu vào.
  5. Đưa ra khuyến nghị phải dựa trực tiếp trên số liệu được cung cấp.
  ```
- **Đánh giá kết quả**:
  - **Độ chính xác**: 100%. Bám sát chính xác từng trường thông tin trong JSON.
  - **Độ ngắn gọn**: Xuất sắc. Bố cục 4 mục rõ ràng bằng Markdown.
  - **Khả năng bám số liệu**: Tuyệt đối. Trích dẫn chính xác tồn kho, tồn tối thiểu và lượng xuất 30 ngày.
  - **Khả năng phát hiện bất thường**: Phát hiện chính xác sản phẩm `HH001` (Tồn: 5, Min: 10, Export 30 days: 25).
  - **Hiện tượng Hallucination**: **0% (Đã triệt tiêu hoàn toàn)**.

---

## 3. KẾT LUẬN

Phiên bản **Prompt V3** đáp ứng tối đa tiêu chí kiểm tra của học phần AIA331, đảm bảo tính nhất quán dữ liệu và minh bạch nguồn gốc suy luận.
