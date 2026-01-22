from pydantic import BaseModel , ConfigDict
from typing import List

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)

class ProductCreate(BaseModel):
    name: str
    category: str
    price: float
    stock: int

class ProductOut(ProductCreate):
    id: int
    class Config:
        orm_mode = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int

class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
