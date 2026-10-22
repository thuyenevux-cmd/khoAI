from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.models.product import Product
from app.models.inventory import Inventory
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.routers.deps import require_roles
from app.models.user import User

router = APIRouter(prefix="/products", tags=["Products Management"])

def _format_product_response(product: Product) -> dict:
    stock_qty = product.inventory.quantity if product.inventory else 0
    return {
        "id": product.id,
        "code": product.code,
        "name": product.name,
        "category_id": product.category_id,
        "unit_id": product.unit_id,
        "minimum_stock": product.minimum_stock,
        "description": product.description,
        "is_active": product.is_active,
        "created_at": product.created_at,
        "updated_at": product.updated_at,
        "category": product.category,
        "unit": product.unit,
        "current_stock": stock_qty
    }

@router.get("", response_model=List[ProductResponse])
def get_products(
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    is_active: Optional[bool] = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    query = db.query(Product)
    if is_active is not None:
        query = query.filter(Product.is_active == is_active)
    if category_id:
        query = query.filter(Product.category_id == category_id)
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.code.ilike(f"%{search}%")
            )
        )
    products = query.order_by(Product.id.asc()).all()
    return [_format_product_response(p) for p in products]

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "WAREHOUSE", "ACCOUNTANT"]))
):
    p = db.query(Product).filter(Product.id == product_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    return _format_product_response(p)

@router.post("", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    prod_in: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    existing = db.query(Product).filter(Product.code == prod_in.code).first()
    if existing:
        raise HTTPException(status_code=400, detail="Mã sản phẩm đã tồn tại trong CSDL")
    
    product = Product(
        code=prod_in.code,
        name=prod_in.name,
        category_id=prod_in.category_id,
        unit_id=prod_in.unit_id,
        minimum_stock=prod_in.minimum_stock,
        description=prod_in.description,
        is_active=prod_in.is_active
    )
    db.add(product)
    db.flush()

    # Create inventory record
    initial_stock = prod_in.initial_stock if prod_in.initial_stock else 0
    inventory = Inventory(product_id=product.id, quantity=initial_stock)
    db.add(inventory)

    db.commit()
    db.refresh(product)
    return _format_product_response(product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    prod_in: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    for key, val in prod_in.model_dump(exclude_unset=True).items():
        setattr(product, key, val)
        
    db.commit()
    db.refresh(product)
    return _format_product_response(product)

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN"]))
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Không tìm thấy sản phẩm")
    
    # Soft delete
    product.is_active = False
    db.commit()
    return {"success": True, "message": "Xóa mềm sản phẩm thành công (chuyển sang trạng thái ngưng hoạt động)"}
