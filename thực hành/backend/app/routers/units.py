from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.unit import Unit
from app.schemas.unit import UnitResponse, UnitCreate
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/units", tags=["Units Management"])

@router.get("", response_model=List[UnitResponse])
def get_units(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    return db.query(Unit).order_by(Unit.id.asc()).all()

@router.post("", response_model=UnitResponse, status_code=status.HTTP_201_CREATED)
def create_unit(
    unit_in: UnitCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    existing = db.query(Unit).filter(Unit.code == unit_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã đơn vị tính đã tồn tại")
    unit = Unit(code=unit_in.code, name=unit_in.name)
    db.add(unit)
    db.commit()
    db.refresh(unit)
    return unit

@router.delete("/{unit_id}")
def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    unit = db.query(Unit).filter(Unit.id == unit_id).first()
    if not unit:
        raise HTTPException(status_code=404, detail="Không tìm thấy đơn vị tính")
    if unit.products:
        raise HTTPException(status_code=400, detail="Không thể xóa đơn vị tính đang được sử dụng bởi sản phẩm")
    db.delete(unit)
    db.commit()
    return {"success": True, "message": "Xóa đơn vị tính thành công"}
