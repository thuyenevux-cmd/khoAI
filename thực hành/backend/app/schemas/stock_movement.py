from datetime import datetime
from pydantic import BaseModel
from app.schemas.product import ProductResponse
from app.schemas.user import UserResponse

class StockMovementResponse(BaseModel):
    id: int
    product_id: int
    movement_type: str  # IMPORT, EXPORT
    reference_type: str # IMPORT_RECEIPT, EXPORT_RECEIPT
    reference_id: int
    quantity: int
    created_by: int
    created_at: datetime
    product: ProductResponse
    user: UserResponse

    class Config:
        from_attributes = True
