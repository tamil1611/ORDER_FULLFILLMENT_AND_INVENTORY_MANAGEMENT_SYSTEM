from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AuditLog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    action: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    entity_id: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    ip_address: Mapped[str | None] = mapped_column(
        String(45),
        nullable=True
    )

    log_metadata: Mapped[dict | None] = mapped_column(
        JSON,
        nullable=True
    )