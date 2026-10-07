from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user, require_role
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse,ProductUpdate
from app.services.product_service import (
    create_new_product,
    deactivate_existing_product,
    get_product,
    update_existing_product,
    activate_existing_product,
    get_products
)


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.post(
    "/",
    response_model=ProductResponse,
    status_code=status.HTTP_201_CREATED
)
def create_product(
    product_data: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        current_user_id: int = current_user.id  # type: ignore[assignment]

        return create_new_product(
            db=db,
            name=product_data.name,
            sku=product_data.sku,
            description=product_data.description,
            price=product_data.price,
            user_id=current_user_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get(
    "/{product_id}",
    response_model=ProductResponse
)
def get_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        return get_product(
            db=db,
            product_id=product_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
        

@router.put(
    "/{product_id}",
    response_model=ProductResponse
)
def update_product_by_id(
    product_id: int,
    product_data: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        current_user_id: int = current_user.id  # type: ignore[assignment]
        return update_existing_product(
         db=db,
            product_id=product_id,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            user_id=current_user_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
 
@router.patch(
    "/{product_id}/activate",
    response_model=ProductResponse
)
def activate_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return activate_existing_product(
            db=db,
            product_id=product_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
@router.patch(
    "/{product_id}/deactivate",
    response_model=ProductResponse
)
def deactivate_product_by_id(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role("admin")
    )
):
    try:
        return deactivate_existing_product(
            db=db,
            product_id=product_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
        
@router.get(
    "/",
    response_model=list[ProductResponse]
)
def list_products(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_products(db=db)