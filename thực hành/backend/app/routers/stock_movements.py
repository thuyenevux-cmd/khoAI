from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.stock_movement import StockMovement
from app.schemas.stock_movement import StockMovementResponse
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/stock-movements", tags=["Stock Movement Audit Trail"])

@router.get("", response_model=List[StockMovementResponse])
def get_stock_movements(
    product_id: Optional[int] = None,
    movement_type: Optional[str] = None,  # IMPORT, EXPORT
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    query = db.query(StockMovement)
    if product_id:
        query = query.filter(StockMovement.product_id == product_id)
    if movement_type:
        query = query.filter(StockMovement.movement_type == movement_type)
        
    movements = query.order_by(StockMovement.id.desc()).limit(200).all()
    results = []

    for m in movements:
        p = m.product
        stock_qty = p.inventory.quantity if p.inventory else 0
        prod_dict = {
            "id": p.id,
            "code": p.code,
            "name": p.name,
            "category_id": p.category_id,
            "unit_id": p.unit_id,
            "minimum_stock": p.minimum_stock,
            "description": p.description,
            "is_active": p.is_active,
            "created_at": p.created_at,
            "updated_at": p.updated_at,
            "category": p.category,
            "unit": p.unit,
            "current_stock": stock_qty
        }
        results.append({
            "id": m.id,
            "product_id": m.product_id,
            "movement_type": m.movement_type,
            "reference_type": m.reference_type,
            "reference_id": m.reference_id,
            "quantity": m.quantity,
            "created_by": m.created_by,
            "created_at": m.created_at,
            "product": prod_dict,
            "user": m.user
        })

    return results
