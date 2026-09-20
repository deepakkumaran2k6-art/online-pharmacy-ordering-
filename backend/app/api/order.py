from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.core.database import get_db
from app.api.auth import get_current_user_payload
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.medicine import Medicine


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


class OrderItemRequest(BaseModel):
    medicine_id: int
    quantity: int


class CreateOrderRequest(BaseModel):
    delivery_address: str
    items: list[OrderItemRequest]


@router.post("/")
def create_order(
    order_data: CreateOrderRequest,
    db: Session = Depends(get_db),
    user=Depends(get_current_user_payload)
):
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one medicine"
        )

    if not order_data.delivery_address.strip():
        raise HTTPException(
            status_code=400,
            detail="Delivery address is required"
        )

    total_amount = 0
    order_items_data = []

    for item in order_data.items:

        if item.quantity <= 0:
            raise HTTPException(
                status_code=400,
                detail="Quantity must be greater than zero"
            )

        medicine = (
            db.query(Medicine)
            .filter(Medicine.medicine_id == item.medicine_id)
            .first()
        )

        if not medicine:
            raise HTTPException(
                status_code=404,
                detail=f"Medicine {item.medicine_id} not found"
            )

        if medicine.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {medicine.medicine_name}"
            )

        subtotal = medicine.price * item.quantity
        total_amount += subtotal

        order_items_data.append({
            "medicine": medicine,
            "quantity": item.quantity,
            "unit_price": medicine.price,
            "subtotal": subtotal
        })

    new_order = Order(
        user_id=user.get("user_id"),
        total_amount=total_amount,
        order_status="Placed",
        delivery_address=order_data.delivery_address.strip()
    )

    db.add(new_order)
    db.flush()

    for item_data in order_items_data:

        order_item = OrderItem(
            order_id=new_order.order_id,
            medicine_id=item_data["medicine"].medicine_id,
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"],
            subtotal=item_data["subtotal"]
        )

        item_data["medicine"].stock_quantity -= item_data["quantity"]

        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order placed successfully",
        "order_id": new_order.order_id,
        "user_id": new_order.user_id,
        "total_amount": new_order.total_amount,
        "order_status": new_order.order_status,
        "delivery_address": new_order.delivery_address
    }

@router.get("/")
def get_my_orders(
    db: Session = Depends(get_db),
    user=Depends(get_current_user_payload)
):
    orders = (
        db.query(Order)
        .filter(Order.user_id == user.get("user_id"))
        .order_by(Order.order_date.desc())
        .all()
    )

    return orders