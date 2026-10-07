from sqlalchemy.orm import Session
from app.repositories.inventory_repository import get_inventory,create_inventory
from app.repositories.inventory_transaction_repository import create_inventory_transaction
from app.repositories.product_repository import (
    create_product,
    get_product_by_sku,
    get_product_by_id,
    update_product,
    activate_product,
    deactivate_product,
    get_all_products,
   
    
)

from app.repositories.warehouse_repository import get_warehouse_by_id
from app.services.notification_service import create_notification
from app.services.audit_log_service import log_action

def create_new_product(
    db: Session,
    name: str,
    sku: str,
    description: str | None,
    price,
    user_id:int
):
    # Check duplicate SKU
    existing_product = get_product_by_sku(
        db=db,
        sku=sku
    )

    if existing_product:
        raise ValueError("SKU already exists")

    # Create product
    product = create_product(
    db=db,
    name=name,
    sku=sku,
    description=description,
    price=price
)

    log_action(
        db=db,
        user_id=user_id,
        action="PRODUCT_CREATED",
        entity="Product",
        entity_id=getattr(product, "id"),
        metadata={
        "name": name,
        "sku": sku
        
    }
)

    db.commit()

    return product

def get_product(
    db: Session,
    product_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    return product


def update_existing_product(
    db: Session,
    product_id: int,
    name: str | None,
    description: str | None,
    price,
    user_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    updated_product = update_product(
        db=db,
        product=product,
        name=name,
        description=description,
        price=price
    )

    log_action(
        db=db,
        user_id=user_id,
        action="PRODUCT_UPDATED",
        entity="Product",
        entity_id=getattr(product, "id"),
        metadata={
            "name": name,
            "description": description,
            "price": float(price) if price is not None else None
        }
    )

    db.commit()

    return updated_product


    
def activate_existing_product(
    db: Session,
    product_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    if bool(product.is_active):
        raise ValueError("Product already active")

    return activate_product(
        db=db,
        product=product
    )
    
def deactivate_existing_product(
    db: Session,
    product_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    if not bool(product.is_active):
        raise ValueError("Product already inactive")

    return deactivate_product(
        db=db,
        product=product
    )
    
def get_products(
    db:Session
):
    return get_all_products(db=db)

def adjust_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    adjustment_amount: int,
    reason: str,
    user_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    if not bool(product.is_active):
        raise ValueError("Product is inactive")

    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    if not bool(warehouse.is_active):
        raise ValueError("Warehouse is inactive")

    inventory = get_inventory(
       db=db,
       product_id=product_id,
       warehouse_id=warehouse_id
    )

    if not inventory:
      if adjustment_amount < 0:
        raise ValueError("Cannot create inventory with negative quantity")

    inventory = create_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        available_quantity=0
    )

    previous_quantity = int(getattr(inventory,"available_quantity"))

    new_quantity = previous_quantity + adjustment_amount

    if new_quantity < 0:
        raise ValueError(
            "Inventory quantity cannot be negative"
        )

    setattr(
        inventory,
        "available_quantity",
        new_quantity
    )

    create_inventory_transaction(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type="ADJUSTMENT",
        quantity=adjustment_amount,
        created_by=user_id,
        reference_entity="Inventory",
        reference_id=getattr(inventory,"id"),
        metadata={
            "previous_quantity": previous_quantity,
            "new_quantity": new_quantity,
            "reason": reason
        }
    )

    db.commit()
    db.refresh(inventory)
    
    
    available_quantity = int(getattr(inventory, "available_quantity"))
    reorder_level = int(getattr(inventory, "reorder_level"))

    if available_quantity <= reorder_level:
       create_notification(
        db=db,
        user_id=user_id,
        title="Low Stock",
        message=(
            f"Product {product_id} is low in stock. "
            f"Available quantity: {available_quantity}, "
            f"Reorder level: {reorder_level}."
        ),
        notification_type="LOW_STOCK"
    )

    return inventory