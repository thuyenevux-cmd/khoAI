# MINH CHỨNG 01 – SỬ DỤNG AI TRONG PHÂN TÍCH NGHIỆP VỤ KHO

---

## 1. PROMPT GỬI AI
> *"Hãy hỗ trợ tôi phân tích luồng nghiệp vụ nhập kho, xuất kho và kiểm soát chống tồn kho âm cho một ứng dụng quản lý kho doanh nghiệp nhỏ."*

## 2. KẾT QUẢ AI TRẢ VỀ
- Đề xuất mô hình giao dịch ACID Transaction.
- Đề xuất khóa dòng Pessimistic Locking (`SELECT FOR UPDATE`) khi thực hiện xuất kho.

## 3. SINH VIÊN RÀ SOÁT & ĐÁNH GIÁ (STUDENT REVIEW)
- Ý tưởng sử dụng Lock dòng là hoàn toàn chuẩn xác nhằm ngăn race condition khi 2 thủ kho cùng xuất 1 mặt hàng.

## 4. CHỈNH SỬA CỦA SINH VIÊN (STUDENT MODIFICATION)
- Bổ sung thêm bảng `stock_movements` để phục vụ khả năng truy vết nhật ký Audit Log.

## 5. KẾT QUẢ CUỐI CÙNG
Áp dụng thành công vào kiến trúc CSDL và Service Layer của hệ thống.
