from pydantic import BaseModel, ConfigDict, Field


class InventoryResponse(BaseModel):
    id: int
    product_id: int
    warehouse_id: int
    available_quantity: int
    reserved_quantity: int
    damaged_quantity: int
    reorder_level: int
    updated_at: object

    model_config = ConfigDict(
        from_attributes=True
    )
    
class InventoryAdjustRequest(BaseModel):
    product_id: int = Field(gt=0)

    warehouse_id: int = Field(gt=0)

    adjustment_amount: int

    reason: str = Field(
        min_length=3,
        max_length=255
    )
    
class InventoryTransferRequest(BaseModel):
    product_id: int = Field(gt=0)

    from_warehouse_id: int = Field(gt=0)

    to_warehouse_id: int = Field(gt=0)

    quantity: int = Field(gt=0)