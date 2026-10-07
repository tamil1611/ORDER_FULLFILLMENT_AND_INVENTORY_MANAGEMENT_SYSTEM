from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy.orm import relationship

class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_number: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    warehouse_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("warehouses.id"),
        nullable=False
    )

    total_amount: Mapped[float] = mapped_column(
        Float,
        nullable=False,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="PENDING"
    )

    payment_status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default="PENDING"
    )

    expected_delivery_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    
    items = relationship(
    "OrderItem",
    back_populates="order"
)