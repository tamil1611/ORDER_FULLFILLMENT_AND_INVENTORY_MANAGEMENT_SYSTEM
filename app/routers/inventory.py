import json

from fastapi import APIRouter, Depends, HTTPException, Header, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.inventory import (
    InventoryResponse,
    InventoryAdjustRequest,
    InventoryTransferRequest
)
from app.services import inventory_service
from app.services.idempotency_service import check_idempotency, generate_request_hash, save_idempotency_response
from app.services.inventory_service import get_all_inventory_records
from app.services.inventory_service import (
    get_product_inventory as get_product_inventory_service
)
from app.services.inventory_service import adjust_inventory

router = APIRouter(
    prefix="/inventory",
    tags=["Inventory"]
)


@router.get("/", response_model=list[InventoryResponse])
def get_inventory(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_all_inventory_records(db=db)


@router.get("/{product_id}", response_model=list[InventoryResponse])
def get_product_inventory(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_product_inventory_service(db=db,product_id=product_id)


@router.post("/adjust", response_model=InventoryResponse)
def adjust_inventory_api(
    inventory_data: InventoryAdjustRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin", "warehouse_manager")
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key"
    ),
):
    try:
        current_user_id: int = current_user.id  # type: ignore[assignment]

        request_hash = generate_request_hash(
            inventory_data.model_dump()
        )

        existing = check_idempotency(
            db=db,
            key=idempotency_key,
            endpoint="/api/inventory/adjust",
            user_id=current_user_id,
            request_hash=request_hash,
        )

        if existing is not None:
            return json.loads(str(existing.response_body))

        inventory = adjust_inventory(
            db=db,
            product_id=inventory_data.product_id,
            warehouse_id=inventory_data.warehouse_id,
            adjustment_amount=inventory_data.adjustment_amount,
            reason=inventory_data.reason,
            user_id=current_user_id,
        )

        response = InventoryResponse.model_validate(inventory)

        save_idempotency_response(
            db=db,
            key=idempotency_key,
            endpoint="/api/inventory/adjust",
            user_id=current_user_id,
            request_hash=request_hash,
            response_status=200,
            response_body=response.model_dump(mode="json"),
        )

        db.commit()

        return response

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

@router.post("/transfer")
def transfer_inventory(
    inventory_data: InventoryTransferRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin", "warehouse_manager")
    ),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key"
    )
):
    try:
        current_user_id: int = current_user.id  # type: ignore[assignment]

        # Generate request hash
        request_hash = generate_request_hash(
            inventory_data.model_dump()
        )

        # Check existing idempotency key
        existing = check_idempotency(
            db=db,
            key=idempotency_key,
            endpoint="/api/inventory/transfer",
            user_id=current_user_id,
            request_hash=request_hash,
        )

        # If same request was already processed
        if existing is not None:
            return json.loads(
                str(existing.response_body)
            )

        # Perform inventory transfer
        result = inventory_service.transfer_inventory(
            db=db,
            product_id=inventory_data.product_id,
            from_warehouse_id=inventory_data.from_warehouse_id,
            to_warehouse_id=inventory_data.to_warehouse_id,
            quantity=inventory_data.quantity,
            user_id=current_user_id
        )

        # Save response for idempotency
        save_idempotency_response(
            db=db,
            key=idempotency_key,
            endpoint="/api/inventory/transfer",
            user_id=current_user_id,
            request_hash=request_hash,
            response_status=200,
            response_body=result,
        )

        db.commit()

        return result

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )