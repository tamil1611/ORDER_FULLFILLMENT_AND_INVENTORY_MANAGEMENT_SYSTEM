from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReturnCreate(BaseModel):
    order_id: int
    reason: str


class ReturnResponse(BaseModel):
    id: int
    order_id: int
    customer_id: int
    reason: str
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)