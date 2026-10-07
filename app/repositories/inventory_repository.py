from sqlalchemy.orm import Session

from app.models.inventory import Inventory


def get_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int
):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id,
            Inventory.warehouse_id == warehouse_id
        )
        .first()
    )


def get_inventory_by_product(
    db: Session,
    product_id: int
):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id
        )
        .order_by(Inventory.id.desc())
        .all()
    )


def get_all_inventory(
    db: Session
):
    return (
        db.query(Inventory)
        .order_by(Inventory.id.desc())
        .all()
    )


def create_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    available_quantity: int,
    reorder_level: int = 0
):
    inventory = Inventory(
        product_id=product_id,
        warehouse_id=warehouse_id,
        available_quantity=available_quantity,
        reserved_quantity=0,
        damaged_quantity=0,
        reorder_level=reorder_level
    )

    db.add(inventory)
    db.commit()
    db.refresh(inventory)

    return inventory

def get_inventory_for_update(
    db: Session,
    product_id: int,
    warehouse_id: int
):
    return (
        db.query(Inventory)
        .filter(
            Inventory.product_id == product_id,
            Inventory.warehouse_id == warehouse_id
        )
        .with_for_update()
        .order_by(Inventory.reserved_quantity.desc())
        .first()
    )