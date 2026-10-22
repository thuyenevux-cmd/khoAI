from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.category import CategoryResponse
from app.schemas.unit import UnitResponse

class ProductBase(BaseModel):
    code: str = Field(..., min_length=2, max_length=50)
    name: str = Field(..., min_length=2, max_length=150)
    category_id: int
    unit_id: int
    minimum_stock: int = Field(0, ge=0)
    description: Optional[str] = None
    is_active: bool = True

class ProductCreate(ProductBase):
    initial_stock: Optional[int] = Field(0, ge=0)

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category_id: Optional[int] = None
    unit_id: Optional[int] = None
    minimum_stock: Optional[int] = Field(None, ge=0)
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: CategoryResponse
    unit: UnitResponse
    current_stock: int = 0

    class Config:
        from_attributes = True
