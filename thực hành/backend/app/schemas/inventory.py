from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from app.schemas.product import ProductResponse

class InventoryResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    updated_at: datetime
    product: ProductResponse
    status: str = "NORMAL" # NORMAL, LOW_STOCK, OUT_OF_STOCK

    class Config:
        from_attributes = True

class LowStockAlertResponse(BaseModel):
    product_id: int
    product_code: str
    product_name: str
    current_stock: int
    minimum_stock: int
    export_30_days: int
    status: str
