from pydantic import BaseModel, ConfigDict, Field


class WarehouseCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=150
    )

    code: str = Field(
        min_length=1,
        max_length=50
    )

    address: str = Field(
        min_length=5
    )


class WarehouseUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150
    )

    address: str | None = Field(
        default=None,
        min_length=5
    )


class WarehouseResponse(BaseModel):
    id: int
    name: str
    code: str
    address: str
    is_active: bool

    model_config = ConfigDict(
        from_attributes=True
    )