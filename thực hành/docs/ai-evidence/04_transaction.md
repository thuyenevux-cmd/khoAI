# MINH CHỨNG 04 – SỬ DỤNG AI THIẾT KẾ DB TRANSACTION & ANTI-NEGATIVE STOCK

---

## 1. PROMPT GỬI AI
> *"Viết giúp tôi hàm FastAPI xử lý xuất kho trong SQLAlchemy sao cho nếu số lượng xuất vượt quá tồn kho thì rollback và trả về lỗi 400."*

## 2. CODE AI SINH RA (AI GENERATED CODE)
```python
@router.post("/exports")
def create_export(receipt_in: ExportReceiptCreate, db: Session = Depends(get_db)):
    for item in receipt_in.details:
        inv = db.query(Inventory).filter(Inventory.product_id == item.product_id).first()
        if inv.quantity < item.quantity:
            raise HTTPException(400, "Không đủ hàng")
        inv.quantity -= item.quantity
    db.commit()
```

## 3. SINH VIÊN RÀ SOÁT & ĐÁNH GIÁ (STUDENT REVIEW)
- Code của AI chưa có `with_for_update()` nên dễ gặp race condition khi nhiều người cùng thao tác đồng thời.
- Code của AI thiếu xử lý ngoại lệ `db.rollback()` và chưa ghi vào bảng `stock_movements`.

## 4. CHỈNH SỬA VÀ TỐI ƯU CỦA SINH VIÊN (STUDENT MODIFICATION)
- Bổ sung `with_for_update()` (cho MySQL/Postgres) hoặc `db.get_bind()`.
- Bổ sung ghi log `StockMovement` và bọc toàn bộ khối lệnh trong `try...except` với `db.rollback()`.

## 5. KẾT QUẢ CUỐI CÙNG
Hàm `create_export_receipt` hoàn chỉnh trong `backend/app/routers/exports.py` vượt qua 100% test case Pytest chống tồn kho âm.
