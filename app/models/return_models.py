from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class Return(Base):
    __tablename__ = "returns"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False
    )

    customer_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    reason: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        default="REQUESTED",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )