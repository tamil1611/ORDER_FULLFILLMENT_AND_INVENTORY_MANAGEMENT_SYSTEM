from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogResponse(BaseModel):
    id: int
    user_id: int | None = None
    action: str
    entity: str
    entity_id: int | None = None
    timestamp: datetime
    ip_address: str | None = None
    log_metadata: dict | None = None

    model_config = ConfigDict(from_attributes=True)