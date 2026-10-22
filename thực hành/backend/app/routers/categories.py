from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryResponse, CategoryCreate, CategoryUpdate
from app.routers.deps import get_current_user, require_roles
from app.models.user import User

router = APIRouter(prefix="/categories", tags=["Categories Management"])

@router.get("", response_model=List[CategoryResponse])
def get_categories(
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    query = db.query(Category)
    if search:
        query = query.filter(Category.name.ilike(f"%{search}%") | Category.code.ilike(f"%{search}%"))
    return query.order_by(Category.id.asc()).all()

@router.post("", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(
    cat_in: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    existing = db.query(Category).filter(Category.code == cat_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã nhóm hàng đã tồn tại")
    cat = Category(code=cat_in.code, name=cat_in.name, description=cat_in.description)
    db.add(cat)
    db.commit()
    db.refresh(cat)
    return cat

@router.put("/{cat_id}", response_model=CategoryResponse)
def update_category(
    cat_id: int,
    cat_in: CategoryUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhóm hàng")
    if cat_in.name is not None:
        cat.name = cat_in.name
    if cat_in.description is not None:
        cat.description = cat_in.description
    db.commit()
    db.refresh(cat)
    return cat

@router.delete("/{cat_id}")
def delete_category(
    cat_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    cat = db.query(Category).filter(Category.id == cat_id).first()
    if not cat:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhóm hàng")
    if cat.products:
        raise HTTPException(status_code=400, detail="Không thể xóa nhóm hàng đang chứa sản phẩm")
    db.delete(cat)
    db.commit()
    return {"success": True, "message": "Xóa nhóm hàng thành công"}
