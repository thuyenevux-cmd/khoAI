from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.user import UserResponse
from app.schemas.supplier import SupplierResponse
from app.schemas.product import ProductResponse

# --- Import Receipt Schemas ---

class ImportDetailCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: float = Field(0.0, ge=0.0)

class ImportDetailResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float = 0.0
    product: ProductResponse

    class Config:
        from_attributes = True

class ImportReceiptCreate(BaseModel):
    supplier_id: int
    receipt_date: Optional[datetime] = None
    note: Optional[str] = None
    details: List[ImportDetailCreate] = Field(..., min_items=1)

class ImportReceiptResponse(BaseModel):
    id: int
    receipt_code: str
    supplier_id: int
    created_by: int
    receipt_date: datetime
    note: Optional[str] = None
    status: str
    supplier: SupplierResponse
    creator: UserResponse
    details: List[ImportDetailResponse]
    total_amount: float = 0.0

    class Config:
        from_attributes = True

# --- Export Receipt Schemas ---

class ExportDetailCreate(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)

class ExportDetailResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    product: ProductResponse

    class Config:
        from_attributes = True

class ExportReceiptCreate(BaseModel):
    receiver: Optional[str] = None
    receipt_date: Optional[datetime] = None
    note: Optional[str] = None
    details: List[ExportDetailCreate] = Field(..., min_items=1)

class ExportReceiptResponse(BaseModel):
    id: int
    receipt_code: str
    created_by: int
    receipt_date: datetime
    receiver: Optional[str] = None
    note: Optional[str] = None
    status: str
    creator: UserResponse
    details: List[ExportDetailResponse]

    class Config:
        from_attributes = True
