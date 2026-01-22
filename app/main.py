from fastapi import FastAPI
from app.database import Base, engine

import app.models # Ensure models are imported so that
from routers import users, products, orders

app = FastAPI(title="Inventory Management API")
Base.metadata.create_all(bind=engine)

app.include_router(users.router)
app.include_router(products.router)
app.include_router(orders.router)
