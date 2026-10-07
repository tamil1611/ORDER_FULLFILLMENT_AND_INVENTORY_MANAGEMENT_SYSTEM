import pytest

from app.database import SessionLocal
from app.services.order_service import create_order
from app.schemas.order import OrderCreate, OrderItemCreate
from app.models.user import User
from app.models.notification import Notification


def test_order_quantity_validation():
    db = SessionLocal()

    try:
        order_data = OrderCreate(
            warehouse_id=2,
            items=[
                OrderItemCreate(
                    product_id=5,
                    quantity=0
                )
            ]
        )

        with pytest.raises(
            ValueError,
            match="Quantity must be greater than zero"
        ):
            create_order(
                db=db,
                customer_id=7,
                order_data=order_data
            )

    finally:
        db.close()
        
def test_insufficient_inventory():
    db = SessionLocal()

    try:
        order_data = OrderCreate(
            warehouse_id=2,
            items=[
                OrderItemCreate(
                    product_id=5,
                    quantity=999999
                )
            ]
        )

        with pytest.raises(
            ValueError,
            match="Insufficient inventory"
        ):
            create_order(
                db=db,
                customer_id=7,
                order_data=order_data
            )

    finally:
        db.close()
        
def test_product_not_found():
    db = SessionLocal()

    try:
        order_data = OrderCreate(
            warehouse_id=2,
            items=[
                OrderItemCreate(
                    product_id=99999,
                    quantity=1
                )
            ]
        )

        with pytest.raises(
            ValueError,
            match="Product not found"
        ):
            create_order(
                db=db,
                customer_id=7,
                order_data=order_data
            )

    finally:
        db.close()