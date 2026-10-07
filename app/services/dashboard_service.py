from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, date
from app.models.order import Order
from app.models.inventory import Inventory
from app.models.product import Product


def get_admin_dashboard(db: Session):

    total_orders = db.query(Order).count()

    pending_orders = (
        db.query(Order)
        .filter(Order.status == "PENDING")
        .count()
    )

    processing_orders = (
        db.query(Order)
        .filter(
            Order.status.in_(
                ["CONFIRMED", "ASSIGNED", "FULFILLED", "SHIPPED"]
            )
        )
        .count()
    )

    completed_orders = (
        db.query(Order)
        .filter(Order.status == "DELIVERED")
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(Order.status == "CANCELLED")
        .count()
    )

    total_revenue = (
        db.query(func.coalesce(func.sum(Order.total_amount), 0))
        .filter(Order.status == "DELIVERED")
        .scalar()
    )

    low_stock_products = (
        db.query(Inventory)
        .filter(
            Inventory.available_quantity <= Inventory.reorder_level,
            Inventory.available_quantity > 0
        )
        .count()
    )

    out_of_stock_products = (
        db.query(Inventory)
        .filter(Inventory.available_quantity == 0)
        .count()
    )

    return {
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "processing_orders": processing_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_revenue": float(total_revenue or 0),
        "low_stock_products": low_stock_products,
        "out_of_stock_products": out_of_stock_products,
    }
    
    
def get_warehouse_manager_dashboard(
    db: Session,
    warehouse_id: int
):
    # Total available inventory in this warehouse
    warehouse_inventory = (
        db.query(
            func.coalesce(
                func.sum(Inventory.available_quantity),
                0
            )
        )
        .filter(
            Inventory.warehouse_id == warehouse_id
        )
        .scalar()
    )

    # Orders waiting for fulfillment
    pending_fulfillment = (
        db.query(Order)
        .filter(
            Order.warehouse_id == warehouse_id,
            Order.status.in_(["PENDING", "CONFIRMED", "ASSIGNED"])
        )
        .count()
    )

    # Orders currently being processed
    processing_orders = (
        db.query(Order)
        .filter(
            Order.warehouse_id == warehouse_id,
            Order.status.in_(["FULFILLED", "SHIPPED"])
        )
        .count()
    )

    # Low stock items
    low_stock_items = (
        db.query(Inventory)
        .filter(
            Inventory.warehouse_id == warehouse_id,
            Inventory.available_quantity <= Inventory.reorder_level,
            Inventory.available_quantity > 0
        )
        .count()
    )

    # Today's shipments
    today = date.today()

    todays_shipments = (
        db.query(Order)
        .filter(
            Order.warehouse_id == warehouse_id,
            Order.status == "SHIPPED",
            func.date(Order.updated_at) == today
        )
        .count()
    )

    return {
        "warehouse_id": warehouse_id,
        "warehouse_inventory": int(warehouse_inventory or 0),
        "pending_fulfillment": pending_fulfillment,
        "processing_orders": processing_orders,
        "low_stock_items": low_stock_items,
        "todays_shipments": todays_shipments,
    }
    
def get_customer_dashboard(
    db: Session,
    customer_id: int
):
    total_orders = (
        db.query(Order)
        .filter(Order.customer_id == customer_id)
        .count()
    )

    active_orders = (
        db.query(Order)
        .filter(
            Order.customer_id == customer_id,
            Order.status.in_(
                [
                    "PENDING",
                    "CONFIRMED",
                    "ASSIGNED",
                    "FULFILLED",
                    "SHIPPED"
                ]
            )
        )
        .count()
    )

    completed_orders = (
        db.query(Order)
        .filter(
            Order.customer_id == customer_id,
            Order.status == "DELIVERED"
        )
        .count()
    )

    cancelled_orders = (
        db.query(Order)
        .filter(
            Order.customer_id == customer_id,
            Order.status == "CANCELLED"
        )
        .count()
    )

    total_spending = (
        db.query(
            func.coalesce(
                func.sum(Order.total_amount),
                0
            )
        )
        .filter(
            Order.customer_id == customer_id,
            Order.status == "DELIVERED"
        )
        .scalar()
    )

    return {
        "customer_id": customer_id,
        "total_orders": total_orders,
        "active_orders": active_orders,
        "completed_orders": completed_orders,
        "cancelled_orders": cancelled_orders,
        "total_spending": float(total_spending or 0),
    }