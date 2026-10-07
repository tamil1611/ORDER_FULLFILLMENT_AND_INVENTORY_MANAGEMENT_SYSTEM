from sqlalchemy import Float, ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    order_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("orders.id"),
        nullable=False,
        index=True
    )

    product_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("products.id"),
        nullable=False
    )

    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )

    unit_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )

    total_price: Mapped[float] = mapped_column(
        Float,
        nullable=False
    )
    
    
    order = relationship(
    "Order",
    back_populates="items"
)