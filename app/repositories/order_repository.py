from sqlalchemy.orm import Session

from app.models.order import Order


def create_order(
    db: Session,
    order: Order
) -> Order:
    db.add(order)
    db.flush()
    return order


def get_order_by_id(
    db: Session,
    order_id: int
) -> Order | None:
    return (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )


def get_order_by_number(
    db: Session,
    order_number: str
) -> Order | None:
    return (
        db.query(Order)
        .filter(Order.order_number == order_number)
        .first()
    )


def get_customer_orders(
    db: Session,
    customer_id: int,
    page: int = 1,
    page_size: int = 20,
    status: str | None = None,
    warehouse_id:int|None=None,
    payment_status:str|None=None,
    min_total_amount: float | None = None,
    max_total_amount: float | None = None,
) -> list[Order]:

    query = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
    )

    if status:
        query = query.filter(Order.status == status.upper())
        
    if warehouse_id:
        query=query.filter(Order.warehouse_id==warehouse_id)
        
    if payment_status:
        query=query.filter(Order.payment_status==payment_status)
        
    if min_total_amount:
        query=query.filter(Order.min_total_amount==min_total_amount)
        
    if max_total_amount:
        query=query.filter(Order.max_total_amount==max_total_amount)

    offset = (page - 1) * page_size

    return (
        query
        .order_by(Order.created_at.desc())
        .offset(offset)
        .limit(page_size)
        .all()
    )