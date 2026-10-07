from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
    Enum,
    JSON
)
from sqlalchemy.sql import func

from app.database import Base


class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    warehouse_id = Column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False,
        index=True
    )

    transaction_type = Column(
        Enum(
            "PURCHASE",
            "SALE",
            "RESERVATION",
            "RELEASE",
            "ADJUSTMENT",
            "TRANSFER_IN",
            "TRANSFER_OUT",
            "RETURN",
            "DAMAGE",
            name="inventory_transaction_type"
        ),
        nullable=False
    )

    quantity = Column(
        Integer,
        nullable=False
    )

    reference_entity = Column(
        String(100),
        nullable=True
    )

    reference_id = Column(
        Integer,
        nullable=True
    )

    created_by = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )

    transaction_metadata = Column(
        JSON,
        nullable=True
    )