from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class StockMovement(Base):
    __tablename__ = "stock_movements"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    movement_type = Column(String(20), nullable=False)  # IMPORT, EXPORT
    reference_type = Column(String(50), nullable=False) # IMPORT_RECEIPT, EXPORT_RECEIPT
    reference_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)

    product = relationship("Product", back_populates="movements")
    user = relationship("User")
