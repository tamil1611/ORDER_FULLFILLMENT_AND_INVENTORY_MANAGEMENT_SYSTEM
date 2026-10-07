from sqlalchemy.orm import Session
import uuid

from app.models.inventory_transaction import InventoryTransaction
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.product import Product

from app.repositories import (
    inventory_repository,
    inventory_transaction_repository,
    order_repository,
    order_item_repository,
)

from app.schemas.order import OrderCreate
from app.services import inventory_service
from app.services.notification_service import create_notification
from app.models.warehouse import Warehouse

from app.services.audit_log_service import log_action

def create_order(
    db: Session,
    customer_id: int,
    order_data: OrderCreate
) -> Order:

    try:
        order = Order(
            order_number=f"ORD-{uuid.uuid4().hex[:8].upper()}",
            customer_id=customer_id,
            warehouse_id=order_data.warehouse_id,
            total_amount=0,
            status="PENDING",
            payment_status="PENDING",
        )

        order_repository.create_order(db, order)

        total_amount = 0

        for item in order_data.items:

            product = (
                db.query(Product)
                .filter(Product.id == item.product_id)
                .first()
            )

            if not product:
                raise ValueError("Product not found")

            if item.quantity <= 0:
                raise ValueError(
                    "Quantity must be greater than zero"
                )

            inventory_service.reserve_inventory(
                db=db,
                product_id=item.product_id,
                warehouse_id=order_data.warehouse_id,
                quantity=item.quantity,
                order_id=order.id,
                user_id=customer_id
            )

            item_total = float(product.price) * item.quantity

            order_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=item.quantity,
                unit_price=product.price,
                total_price=item_total
            )

            order_item_repository.create_order_item(
                db,
                order_item
            )

            total_amount += item_total

        order.total_amount = total_amount
        
        log_action(
              db=db,
              user_id=customer_id,
              action="ORDER_CREATED",
              entity="Order",
              entity_id=getattr(order, "id"),
              metadata={
                "order_number": order.order_number,
                  "warehouse_id": order_data.warehouse_id,
                "total_amount": total_amount
        }
)

        db.commit()
        db.refresh(order)

        create_notification(
            db=db,
            user_id=customer_id,
            title="Order Created",
            message=(
                f"Your order {order.order_number} "
                "has been created successfully."
            ),
            notification_type="ORDER_CREATED"
        )

        return order

    except Exception as e:
        db.rollback()

        raise ValueError(str(e))

def get_customer_orders(
    db: Session,
    customer_id: int,
    page: int = 1,
    page_size: int = 20,
    status:str|None=None,
    warehouse_id: int|None=None,
    payment_status:str|None=None,
    min_total_amount: float | None = None,
    max_total_amount: float | None = None,
    
) -> list[Order]:
    return order_repository.get_customer_orders(
        db=db,
        customer_id=customer_id,
        page=page,
        page_size=page_size,
        status=status,
        warehouse_id=warehouse_id,
        payment_status=payment_status,
        min_total_amount=min_total_amount,
        max_total_amount=max_total_amount,
    )
    
def confirm_payment(
    db: Session,
    order_id: int,
    payment_reference: str,
    user_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.customer_id != user_id:
        raise ValueError(
            "You are not allowed to confirm payment for this order"
        )

    if order.payment_status == "PAID":
        raise ValueError(
            "Payment has already been confirmed"
        )

    if order.status == "CANCELLED":
        raise ValueError(
            "Cancelled orders cannot be paid"
        )

    if not payment_reference.strip():
        raise ValueError(
            "Payment reference is required"
        )

    order.payment_status = "PAID"

    log_action(
        db=db,
        user_id=user_id,
        action="PAYMENT_CONFIRMED",
        entity="Order",
        entity_id=getattr(order, "id"),
        metadata={
            "order_number": order.order_number,
            "payment_reference": payment_reference
        }
    )

    db.commit()
    db.refresh(order)

    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Payment Confirmed",
        message=(
            f"Payment for order {order.order_number} "
            "has been confirmed."
        ),
        notification_type="PAYMENT_CONFIRMED"
    )

    return order

def confirm_order(
    db: Session,
    order_id: int,
    user_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.status != "PENDING":
        raise ValueError(
            "Only pending orders can be confirmed"
        )

    order.status = "CONFIRMED"
    
    log_action(
    db=db,
    user_id=user_id,
    action="ORDER_STATUS_CHANGED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "old_status": "PENDING",
        "new_status": "CONFIRMED"
    }
)

    db.commit()
    db.refresh(order)

    create_notification(
       db=db,
       user_id=order.customer_id,
       title="Order Confirmed",
       message=f"Your order {order.order_number} has been confirmed.",
       notification_type="ORDER_CONFIRMED"
)

    return order

def fulfill_order(
    db: Session,
    order_id: int,
    user_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.status != "CONFIRMED":
        raise ValueError(
            "Only confirmed orders can be fulfilled"
        )

    order_items = order_item_repository.get_order_items(
        db,
        order.id
    )

    for item in order_items:

        inventory = inventory_repository.get_inventory_for_update(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id
        )

        if not inventory:
            raise ValueError(
                "Inventory not found"
            )

        if inventory.reserved_quantity < item.quantity:
            raise ValueError(
                "Insufficient reserved inventory"
            )

        inventory.reserved_quantity -= item.quantity

        inventory_transaction_repository.create_inventory_transaction(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id,
            transaction_type="SALE",
            quantity=item.quantity,
            created_by=user_id,
            reference_entity="ORDER",
            reference_id=order.id,
            metadata={"reason": "ORDER_FULFILLED"}
        )

    order.status = "FULFILLED"
    
    log_action(
    db=db,
    user_id=user_id,
    action="ORDER_STATUS_CHANGED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "old_status": "CONFIRMED",
        "new_status": "FULFILLED"
    }
)

    db.commit()
    db.refresh(order)

    return order

def ship_order(
    db: Session,
    order_id: int,
    user_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.status != "FULFILLED":
        raise ValueError(
            "Only fulfilled orders can be shipped"
        )

    order.status = "SHIPPED"
    
    log_action(
    db=db,
    user_id=user_id,
    action="ORDER_STATUS_CHANGED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "old_status": "FULFILLED",
        "new_status": "SHIPPED"
    }
)

    db.commit()
    db.refresh(order)

    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Order Shipped",
        message=f"Your order {order.order_number} has been shipped.",
        notification_type="ORDER_SHIPPED"
    )

    return order

def deliver_order(
    db: Session,
    order_id: int,
    user_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.status != "SHIPPED":
        raise ValueError(
            "Only shipped orders can be delivered"
        )

    order.status = "DELIVERED"
    
    log_action(
    db=db,
    user_id=user_id,
    action="ORDER_STATUS_CHANGED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "old_status": "SHIPPED",
        "new_status": "DELIVERED"
    }
)

    db.commit()
    db.refresh(order)

    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Order Delivered",
        message=f"Your order {order.order_number} has been delivered.",
        notification_type="ORDER_DELIVERED"
    )

    return order

def return_order(
    db: Session,
    order_id: int,
    customer_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.customer_id != customer_id:
        raise ValueError(
            "You are not allowed to return this order"
        )

    if order.status not in ["FULFILLED", "DELIVERED"]:
       raise ValueError(
        "Only fulfilled or delivered orders can be returned"
    )
        
    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Return Requested",
        message=f"Return requested for order {order.order_number}.",
        notification_type="RETURN_REQUESTED"
)

    order_items = order_item_repository.get_order_items(
        db,
        order.id
    )

    for item in order_items:

        inventory = inventory_repository.get_inventory_for_update(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id
        )

        if not inventory:
            raise ValueError(
                "Inventory not found"
            )

        inventory.available_quantity += item.quantity

        inventory_transaction_repository.create_inventory_transaction(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id,
            transaction_type="RETURN",
            quantity=item.quantity,
            created_by=customer_id,
            reference_entity="ORDER",
            reference_id=order.id,
            metadata={"reason": "ORDER_RETURNED"}
        )

    order.status = "RETURNED"

    db.commit()
    db.refresh(order)
    
    create_notification(
       db=db,
       user_id=order.customer_id,
       title="Return Approved",
       message=f"Your return for order {order.order_number} has been approved.",
       notification_type="RETURN_APPROVED"
)

    return order


def cancel_order(
    db: Session,
    order_id: int,
    customer_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.customer_id != customer_id:
        raise ValueError(
            "You are not allowed to cancel this order"
        )

    if order.status not in ["PENDING", "CONFIRMED"]:
        raise ValueError(
            "Order cannot be cancelled at this stage"
        )

    order_items = order_item_repository.get_order_items(
        db,
        order.id
    )

    for item in order_items:

        inventory = inventory_repository.get_inventory_for_update(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id
        )

        if not inventory:
            raise ValueError(
                "Inventory not found"
            )

        if inventory.reserved_quantity < item.quantity:
            raise ValueError(
                "Insufficient reserved inventory"
            )

        inventory.reserved_quantity -= item.quantity
        inventory.available_quantity += item.quantity

        inventory_transaction_repository.create_inventory_transaction(
            db=db,
            product_id=item.product_id,
            warehouse_id=order.warehouse_id,
            transaction_type="RELEASE",
            quantity=item.quantity,
            created_by=customer_id,
            reference_entity="ORDER",
            reference_id=order.id,
            metadata={
                "reason": "ORDER_CANCELLED"
            }
        )

        log_action(
            db=db,
            user_id=customer_id,
            action="INVENTORY_RELEASED",
            entity="Inventory",
            entity_id=getattr(inventory, "id"),
            metadata={
                "product_id": item.product_id,
                "warehouse_id": order.warehouse_id,
                "quantity": item.quantity,
                "order_id": order.id,
                "reason": "ORDER_CANCELLED"
            }
        )

    order.status = "CANCELLED"
    
    log_action(
    db=db,
    user_id=customer_id,
    action="ORDER_CANCELLED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "order_number": order.order_number,
        "reason": "CUSTOMER_CANCELLED"
    }
)

    db.commit()
    db.refresh(order)

    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Order Cancelled",
        message=f"Your order {order.order_number} has been cancelled.",
        notification_type="ORDER_CANCELLED"
    )

    return order


def assign_order(
    db: Session,
    order_id: int,
    warehouse_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")
    
    print("ORDER STATUS:", repr(order.status))

    if order.status != "CONFIRMED":
        raise ValueError(
            "Only confirmed orders can be assigned"
        )

    warehouse = (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id)
        .first()
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    order.warehouse_id = warehouse_id
    order.status = "ASSIGNED"
    
    log_action(
    db=db,
    user_id=order.customer_id,
    action="ORDER_ASSIGNED",
    entity="Order",
    entity_id=getattr(order, "id"),
    metadata={
        "warehouse_id": warehouse_id
    }
)

    db.commit()
    db.refresh(order)

    create_notification(
        db=db,
        user_id=order.customer_id,
        title="Order Assigned",
        message=f"Your order {order.order_number} has been assigned.",
        notification_type="ORDER_ASSIGNED"
    )

    return order

def get_order(
    db: Session,
    order_id: int
) -> Order:

    order = order_repository.get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    return order