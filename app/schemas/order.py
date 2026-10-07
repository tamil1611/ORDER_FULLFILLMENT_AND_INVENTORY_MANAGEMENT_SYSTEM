from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int


class OrderCreate(BaseModel):
    warehouse_id: int
    items: list[OrderItemCreate]
    
class PaymentConfirmRequest(BaseModel):
    payment_reference: str


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    total_price: float

    model_config = ConfigDict(from_attributes=True)

class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_id: int
    warehouse_id: int
    total_amount: float
    status: str
    payment_status: str
    expected_delivery_date: datetime | None
    created_at: datetime
    updated_at: datetime
    items: list[OrderItemResponse] = []

    model_config = ConfigDict(from_attributes=True)