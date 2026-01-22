from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models import Order, OrderItem, Product
from app.schema import OrderCreate
from app.dependency import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new order for the logged-in user
    """

    new_order = Order(
        user_id=current_user["id"],
        total_amount=0.0,
        status="PENDING"
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    total_amount = 0.0

    for item in order.items:
        product = db.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=404,
                detail=f"Product {item.product_id} not found"
            )

        if product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for product {product.name}"
            )

        product.stock -= item.quantity

        item_total = product.price * item.quantity
        total_amount += item_total

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=product.id,
            quantity=item.quantity,
            price=item_total
        )
        db.add(order_item)

    new_order.total_amount = total_amount
    db.commit()

    return {
        "order_id": new_order.id,
        "total_amount": total_amount,
        "status": new_order.status
    }


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get order details by order ID
    """

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user["id"]
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order


@router.get("/")
def get_my_orders(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all orders of logged-in user
    """

    orders = db.query(Order).filter(
        Order.user_id == current_user["id"]
    ).all()

    return orders


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Cancel an order (only if PENDING)
    """

    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user["id"]
    ).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status != "PENDING":
        raise HTTPException(
            status_code=400,
            detail="Only pending orders can be cancelled"
        )

    db.delete(order)
    db.commit()

    return None
