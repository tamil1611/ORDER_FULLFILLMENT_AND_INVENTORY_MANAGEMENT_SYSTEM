from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    name: str = Field(min_length=2, max_length=150)
    sku: str = Field(min_length=1, max_length=100)
    description: str | None = None
    price: Decimal = Field(gt=0)


class ProductResponse(BaseModel):
    id: int
    name: str
    sku: str
    description: str | None
    price: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
    
class ProductUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    description: str | None = None

    price: Decimal | None = Field(
        default=None,
        gt=0
    )