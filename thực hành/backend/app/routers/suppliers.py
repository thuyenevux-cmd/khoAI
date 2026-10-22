from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.supplier import Supplier
from app.schemas.supplier import SupplierResponse, SupplierCreate, SupplierUpdate
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/suppliers", tags=["Suppliers Management"])

@router.get("", response_model=List[SupplierResponse])
def get_suppliers(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    query = db.query(Supplier)
    if search:
        query = query.filter(
            Supplier.name.ilike(f"%{search}%") |
            Supplier.code.ilike(f"%{search}%") |
            Supplier.phone.ilike(f"%{search}%")
        )
    return query.order_by(Supplier.id.asc()).all()

@router.post("", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    sup_in: SupplierCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    existing = db.query(Supplier).filter(Supplier.code == sup_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã nhà cung cấp đã tồn tại")
    sup = Supplier(**sup_in.model_dump())
    db.add(sup)
    db.commit()
    db.refresh(sup)
    return sup

@router.put("/{sup_id}", response_model=SupplierResponse)
def update_supplier(
    sup_id: int,
    sup_in: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    sup = db.query(Supplier).filter(Supplier.id == sup_id).first()
    if not sup:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà cung cấp")
    for key, val in sup_in.model_dump(exclude_unset=True).items():
        setattr(sup, key, val)
    db.commit()
    db.refresh(sup)
    return sup

@router.delete("/{sup_id}")
def delete_supplier(
    sup_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    sup = db.query(Supplier).filter(Supplier.id == sup_id).first()
    if not sup:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhà cung cấp")
    if sup.import_receipts:
        raise HTTPException(status_code=400, detail="Không thể xóa nhà cung cấp đã có lịch sử phiếu nhập")
    db.delete(sup)
    db.commit()
    return {"success": True, "message": "Xóa nhà cung cấp thành công"}
