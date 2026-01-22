from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    password = Column(String(255))
    role = Column(String(50), default="user")
    created_at = Column(DateTime, default=datetime.utcnow)

    orders = relationship("Order", back_populates="user")

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    category = Column(String(100))
    price = Column(Float)
    stock = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    total_amount = Column(Float)
    status = Column(String(50), default="PENDING")
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
