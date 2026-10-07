from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User

from app.schemas.warehouse import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseResponse
)

from app.services.warehouse_service import (
    create_new_warehouse,
    get_warehouse,
    update_existing_warehouse,
    deactivate_existing_warehouse,
    activate_existing_warehouse,
    get_warehouses
)


router = APIRouter(
    prefix="/warehouses",
    tags=["Warehouses"]
)

@router.post(
    "/",
    response_model=WarehouseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_warehouse_api(
    warehouse_data: WarehouseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return create_new_warehouse(
            db=db,
            name=warehouse_data.name,
            code=warehouse_data.code,
            address=warehouse_data.address
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.get(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def get_warehouse_api(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
@router.put(
    "/{warehouse_id}",
    response_model=WarehouseResponse
)
def update_warehouse_api(
    warehouse_id: int,
    warehouse_data: WarehouseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return update_existing_warehouse(
            db=db,
            warehouse_id=warehouse_id,
            name=warehouse_data.name,
            address=warehouse_data.address
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        
@router.patch(
    "/{warehouse_id}/deactivate",
    response_model=WarehouseResponse
)
def deactivate_warehouse_api(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return deactivate_existing_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        

@router.patch(
    "/{warehouse_id}/activate",
    response_model=WarehouseResponse
)
def activate_warehouse_api(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return activate_existing_warehouse(
            db=db,
            warehouse_id=warehouse_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.get(
    "/",
    response_model=list[WarehouseResponse]
)
def list_warehouses(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_warehouses(db=db)