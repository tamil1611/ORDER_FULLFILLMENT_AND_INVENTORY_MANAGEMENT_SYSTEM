from sqlalchemy.orm import Session

from app.models.inventory_transaction import InventoryTransaction
from app.repositories import inventory_transaction_repository
from app.repositories import inventory_repository
from app.repositories.inventory_repository import (
    create_inventory,
    get_inventory,
    get_inventory_by_product,
    get_all_inventory
)

from app.repositories.product_repository import get_product_by_id
from app.services.notification_service import create_notification
from app.services.audit_log_service import log_action

def get_inventory_record(
    db: Session,
    product_id: int,
    warehouse_id: int,
    adjustment_amount: int
):
    inventory = get_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id
    )

    if inventory:
        return inventory

    if adjustment_amount < 0:
        raise ValueError(
            "Cannot create inventory with negative quantity"
        )

    inventory = create_inventory(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        available_quantity=adjustment_amount
    )

    return inventory

def get_product_inventory(
    db: Session,
    product_id: int
):
    product = get_product_by_id(
        db=db,
        product_id=product_id
    )

    if not product:
        raise ValueError("Product not found")

    return get_inventory_by_product(
        db=db,
        product_id=product_id
    )


def get_all_inventory_records(
    db: Session
):
    return get_all_inventory(
        db=db
    )

def adjust_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    adjustment_amount: int,
    reason: str | None,
    user_id: int
):
    inventory = get_inventory_record(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        adjustment_amount=adjustment_amount
    )

    inventory.available_quantity += adjustment_amount

    inventory_transaction_repository.create_inventory_transaction(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type="ADJUSTMENT",
        quantity=adjustment_amount,
        created_by=user_id,
        reference_entity="INVENTORY",
        metadata={
            "reason": reason
        }
    )
    
    print("AUDIT LOG START")
    
    log_action(
    db=db,
    user_id=user_id,
    action="INVENTORY_ADJUSTED",
    entity="Inventory",
    entity_id=getattr(inventory, "id"),
    metadata={
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "adjustment_amount": adjustment_amount,
        "reason": reason
    }
)



    db.commit()

    return inventory


    
def reserve_inventory(
    db: Session,
    product_id: int,
    warehouse_id: int,
    quantity: int,
    order_id: int,
    user_id: int
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    inventory = inventory_repository.get_inventory_for_update(
        db=db,
        product_id=product_id,
        warehouse_id=warehouse_id
    )

    if not inventory:
        raise ValueError("Inventory not found")

    if inventory.available_quantity < quantity:
        raise ValueError("Insufficient inventory")

    # Move quantity from available to reserved
    inventory.available_quantity -= quantity
    inventory.reserved_quantity += quantity

    # Record inventory transaction
 

    inventory_transaction_repository.create_inventory_transaction(
    db=db,
    product_id=product_id,
    warehouse_id=warehouse_id,
    transaction_type="RESERVATION",
    quantity=quantity,
    created_by=user_id,
    reference_entity="ORDER",
    reference_id=order_id,
    metadata={"reason": "ORDER_CREATED"}
)
    
    log_action(
    db=db,
    user_id=user_id,
    action="INVENTORY_RESERVED",
    entity="Inventory",
    entity_id=getattr(inventory, "id"),
    metadata={
        "product_id": product_id,
        "warehouse_id": warehouse_id,
        "quantity": quantity,
        "order_id": order_id
    }
)
    return inventory

def transfer_inventory(
    db: Session,
    product_id: int,
    from_warehouse_id: int,
    to_warehouse_id: int,
    quantity: int,
    user_id: int
):
    if quantity <= 0:
        raise ValueError("Quantity must be greater than zero")

    if from_warehouse_id == to_warehouse_id:
        raise ValueError(
            "Source and destination warehouse cannot be same"
        )

    try:
        # Get source inventory with row lock
        source_inventory = inventory_repository.get_inventory_for_update(
            db=db,
            product_id=product_id,
            warehouse_id=from_warehouse_id
        )

        if not source_inventory:
            raise ValueError("Source inventory not found")

        if source_inventory.available_quantity < quantity:
            raise ValueError("Insufficient inventory")

        # Get destination inventory with row lock
        destination_inventory = inventory_repository.get_inventory_for_update(
            db=db,
            product_id=product_id,
            warehouse_id=to_warehouse_id
        )

        # Create destination inventory if it doesn't exist
        if not destination_inventory:
            destination_inventory = inventory_repository.create_inventory(
                db=db,
                product_id=product_id,
                warehouse_id=to_warehouse_id,
                available_quantity=0
            )

        # Update quantities
        source_inventory.available_quantity -= quantity
        destination_inventory.available_quantity += quantity

        # TRANSFER_OUT
        inventory_transaction_repository.create_inventory_transaction(
            db=db,
            product_id=product_id,
            warehouse_id=from_warehouse_id,
            transaction_type="TRANSFER_OUT",
            quantity=quantity,
            created_by=user_id,
            reference_entity="INVENTORY_TRANSFER",
            metadata={
                "to_warehouse_id": to_warehouse_id
            }
        )

        # TRANSFER_IN
        inventory_transaction_repository.create_inventory_transaction(
            db=db,
            product_id=product_id,
            warehouse_id=to_warehouse_id,
            transaction_type="TRANSFER_IN",
            quantity=quantity,
            created_by=user_id,
            reference_entity="INVENTORY_TRANSFER",
            metadata={
                "from_warehouse_id": from_warehouse_id
            }
        )
        
        log_action(
    db=db,
    user_id=user_id,
    action="INVENTORY_TRANSFERRED",
    entity="Inventory",
    entity_id=getattr(destination_inventory, "id"),
    metadata={
        "product_id": product_id,
        "from_warehouse_id": from_warehouse_id,
        "to_warehouse_id": to_warehouse_id,
        "quantity": quantity
    }
)

        # Notification
        create_notification(
            db=db,
            user_id=user_id,
            title="Inventory Transfer",
            message=(
                f"{quantity} units of product {product_id} "
                f"transferred from warehouse {from_warehouse_id} "
                f"to warehouse {to_warehouse_id}."
            ),
            notification_type="INVENTORY_TRANSFER"
        )

        # Save everything together
        db.commit()

        return {
            "message": "Inventory transferred successfully",
            "product_id": product_id,
            "from_warehouse_id": from_warehouse_id,
            "to_warehouse_id": to_warehouse_id,
            "quantity": quantity
        }

    except Exception:
        # If anything fails, undo all changes
        db.rollback()
        raise
    
    
    