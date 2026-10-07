from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, Integer, String, Text

from app.database import Base


class IdempotencyKey(Base):
    __tablename__ = "idempotency_keys"

    id = Column(Integer, primary_key=True, index=True)

    key = Column(String(255), unique=True, nullable=False, index=True)

    endpoint = Column(String(255), nullable=False)

    user_id = Column(Integer, nullable=False, index=True)

    request_hash = Column(String(64), nullable=False)

    response_status = Column(Integer, nullable=False)

    response_body = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )