from sqlalchemy.orm import Session

from app.models.inventory_transaction import InventoryTransaction


def create_inventory_transaction(
    db: Session,
    product_id: int,
    warehouse_id: int,
    transaction_type: str,
    quantity: int,
    created_by: int,
    reference_entity: str | None = None,
    reference_id: int | None = None,
    metadata: dict | None = None
):
    transaction = InventoryTransaction(
        product_id=product_id,
        warehouse_id=warehouse_id,
        transaction_type=transaction_type,
        quantity=quantity,
        created_by=created_by,
        reference_entity=reference_entity,
        reference_id=reference_id,
        transaction_metadata=metadata
    )

    db.add(transaction)
    db.flush()

    return transaction