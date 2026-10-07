from sqlalchemy.orm import Session

from app.models.order_item import OrderItem
from app.repositories import order_item_repository as order_item_repository


def create_order_item(
    db: Session,
    order_item: OrderItem
) -> OrderItem:

    return order_item_repository.create_order_item(
        db,
        order_item
    )


def get_order_items(
    db: Session,
    order_id: int
) -> list[OrderItem]:

    return order_item_repository.get_order_items(
        db,
        order_id
    )