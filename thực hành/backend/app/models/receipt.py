from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class ImportReceipt(Base):
    __tablename__ = "import_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_code = Column(String(50), unique=True, index=True, nullable=False)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    receipt_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    note = Column(String(255), nullable=True)
    status = Column(String(20), default="COMPLETED", nullable=False)

    supplier = relationship("Supplier", back_populates="import_receipts")
    creator = relationship("User")
    details = relationship("ImportReceiptDetail", back_populates="receipt", cascade="all, delete-orphan")


class ImportReceiptDetail(Base):
    __tablename__ = "import_receipt_details"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("import_receipts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)

    receipt = relationship("ImportReceipt", back_populates="details")
    product = relationship("Product", back_populates="import_details")


class ExportReceipt(Base):
    __tablename__ = "export_receipts"

    id = Column(Integer, primary_key=True, index=True)
    receipt_code = Column(String(50), unique=True, index=True, nullable=False)
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    receipt_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    receiver = Column(String(100), nullable=True)
    note = Column(String(255), nullable=True)
    status = Column(String(20), default="COMPLETED", nullable=False)

    creator = relationship("User")
    details = relationship("ExportReceiptDetail", back_populates="receipt", cascade="all, delete-orphan")


class ExportReceiptDetail(Base):
    __tablename__ = "export_receipt_details"

    id = Column(Integer, primary_key=True, index=True)
    receipt_id = Column(Integer, ForeignKey("export_receipts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)

    receipt = relationship("ExportReceipt", back_populates="details")
    product = relationship("Product", back_populates="export_details")
