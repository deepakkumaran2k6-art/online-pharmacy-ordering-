from unittest.mock import MagicMock

import pytest

from app.api.order import create_order, CreateOrderRequest, OrderItemRequest
from app.models.medicine import Medicine


class TestOrderService:

    def test_create_order_success(self):
        db = MagicMock()

        medicine = Medicine(
            medicine_id=1,
            category_id=1,
            medicine_name="Paracetamol",
            description="Used for fever and mild pain relief",
            price=25.00,
            stock_quantity=100,
            prescription_required=False
        )

        db.query.return_value.filter.return_value.first.return_value = medicine

        order_data = CreateOrderRequest(
            delivery_address="Vellore, Tamil Nadu",
            items=[
                OrderItemRequest(
                    medicine_id=1,
                    quantity=2
                )
            ]
        )

        user = {
            "user_id": 1
        }

        result = create_order(
            order_data=order_data,
            db=db,
            user=user
        )

        assert result["message"] == "Order placed successfully"
        assert result["user_id"] == 1
        assert result["total_amount"] == 50.00
        assert result["order_status"] == "Placed"
        assert result["delivery_address"] == "Vellore, Tamil Nadu"

        assert medicine.stock_quantity == 98

        db.add.assert_called()
        db.commit.assert_called_once()


    def test_create_order_empty_items(self):
        db = MagicMock()

        order_data = CreateOrderRequest(
            delivery_address="Vellore, Tamil Nadu",
            items=[]
        )

        user = {
            "user_id": 1
        }

        with pytest.raises(
            Exception,
            match="Order must contain at least one medicine"
        ):
            create_order(
                order_data=order_data,
                db=db,
                user=user
            )


    def test_create_order_invalid_quantity(self):
        db = MagicMock()

        order_data = CreateOrderRequest(
            delivery_address="Vellore, Tamil Nadu",
            items=[
                OrderItemRequest(
                    medicine_id=1,
                    quantity=0
                )
            ]
        )

        user = {
            "user_id": 1
        }

        with pytest.raises(
            Exception,
            match="Quantity must be greater than zero"
        ):
            create_order(
                order_data=order_data,
                db=db,
                user=user
            )


    def test_create_order_medicine_not_found(self):
        db = MagicMock()

        db.query.return_value.filter.return_value.first.return_value = None

        order_data = CreateOrderRequest(
            delivery_address="Vellore, Tamil Nadu",
            items=[
                OrderItemRequest(
                    medicine_id=999,
                    quantity=1
                )
            ]
        )

        user = {
            "user_id": 1
        }

        with pytest.raises(
            Exception,
            match="Medicine 999 not found"
        ):
            create_order(
                order_data=order_data,
                db=db,
                user=user
            )


    def test_create_order_insufficient_stock(self):
        db = MagicMock()

        medicine = Medicine(
            medicine_id=1,
            category_id=1,
            medicine_name="Paracetamol",
            description="Used for fever and mild pain relief",
            price=25.00,
            stock_quantity=1,
            prescription_required=False
        )

        db.query.return_value.filter.return_value.first.return_value = medicine

        order_data = CreateOrderRequest(
            delivery_address="Vellore, Tamil Nadu",
            items=[
                OrderItemRequest(
                    medicine_id=1,
                    quantity=5
                )
            ]
        )

        user = {
            "user_id": 1
        }

        with pytest.raises(
            Exception,
            match="Insufficient stock for Paracetamol"
        ):
            create_order(
                order_data=order_data,
                db=db,
                user=user
            )