from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Product
from app.schema import ProductCreate, ProductOut
from typing import List

router = APIRouter(prefix="/products", tags=["Products"])

@router.post("/", response_model=ProductOut)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    p = Product(**product.dict())
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

@router.get("/", response_model=List[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()
