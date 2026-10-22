# 07. VỊ TRÍ VÀ VAI TRÒ CỦA AI TRONG HỆ THỐNG

---

## 1. VỊ TRÍ CỦA AI TRONG KIẾN TRÚC ỨNG DỤNG

Khác với các ứng dụng tích hợp Chatbot rời rạc không ăn nhập vào nghiệp vụ, trong hệ thống này, **AI được gắn trực tiếp vào quy trình báo cáo và ra quyết định quản lý kho**:

```text
[ CSDL Kho (MySQL/SQLite) ]
          │
          ▼ 1. Truy vấn Dữ liệu Thật (SQL Query)
[ Data Aggregator (Backend Service) ]
          │
          ▼ 2. Đóng gói JSON Snapshot
[ AI Prompt Engine + Template File ]
          │
          ▼ 3. Gửi Payload kèm Rule Chống Bịạ Số liệu
[ OpenAI API / LLM Provider ]
          │
          ▼ 4. Trả về Văn bản Phân tích & Gợi ý
[ Dashboard UI (Kèm Khoang Dữ liệu Nguồn CSDL) ]
```

---

## 2. BA TÍNH NĂNG AI NÒNG CỐT

1. **AI Feature 1 – Sinh Báo cáo Kho theo Tháng**:
   - Tự động đọc tổng số mặt hàng, tổng số lượng nhập/xuất, số sản phẩm tồn dưới mức tối thiểu và danh sách hàng xuất chạy.
   - Xuất ra báo cáo chuyên nghiệp gồm: Tình trạng kho, Hàng cần chú ý, Điểm bất thường, Khuyến nghị vận hành.
2. **AI Feature 2 – Gợi ý Nhập Hàng**:
   - Dựa trên công thức tốc độ xuất hàng ngày: `burn_rate = export_30_days / 30`.
   - Dự báo thời gian còn lại trước khi hết hàng: `days_remaining = current_stock / burn_rate`.
   - Đưa ra danh sách ưu tiên nhập hàng (Mức Ưu tiên: Cao / Trung bình / Thấp) kèm lý do và số lượng đề xuất tham khảo.
3. **AI Feature 3 – Tóm tắt Biến động Bất thường**:
   - Nhận diện các mặt hàng xuất đột biến trong 30 ngày gần đây so với kỳ trước.
   - Nhận diện hàng tồn kho lâu ngày không phát sinh giao dịch xuất hàng.

---

## 3. NGUYÊN TẮC BẢO VỆ VÀ RÀNG BUỘC AI (AI SAFETY & HALLUCINATION CONTROL)

- **Nguyên tắc Ground Truth**: AI **CHỈ** được phân tích số liệu nằm trong khối dữ liệu JSON được truyền từ backend. Tuyệt đối không tự sáng tác thêm sản phẩm hoặc con số ngẫu nhiên.
- **Bảo mật Dữ liệu**: Không gửi giá vốn mua hàng nhạy cảm hoặc mật khẩu người dùng lên API AI.
- **Quyền Quyết định Cuối cùng thuộc về Con người**: Kết quả gợi ý của AI mang tính chất tham khảo trợ lý, con người (Thủ kho/Admin) vẫn là người thực hiện thao tác duyệt phiếu nhập hàng thực tế.
