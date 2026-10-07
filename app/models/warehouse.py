from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func

from app.database import Base


class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(150),
        nullable=False
    )

    code = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    address = Column(
        Text,
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )