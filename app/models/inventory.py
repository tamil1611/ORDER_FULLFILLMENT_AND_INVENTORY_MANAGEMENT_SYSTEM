from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Inventory(Base):
    __tablename__ = "inventory"

    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "warehouse_id",
            name="uq_inventory_product_warehouse"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    warehouse_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    available_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    reserved_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    damaged_quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    reorder_level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )