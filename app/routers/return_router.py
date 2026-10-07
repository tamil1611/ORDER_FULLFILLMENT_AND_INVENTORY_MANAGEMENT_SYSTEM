from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.schemas.return_schema import ReturnCreate, ReturnResponse
from app.services.return_service import approve_return, create_return_request


router = APIRouter(
    prefix="/api/returns",
    tags=["Returns"]
)


@router.post(
    "",
    response_model=ReturnResponse,
    status_code=status.HTTP_201_CREATED
)
def create_return(
    return_data: ReturnCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("customer"))
):
    try:
        return create_return_request(
            db=db,
            order_id=return_data.order_id,
            customer_id=int(getattr(current_user, "id")),
            reason=return_data.reason
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
        
        
@router.patch(
    "/{return_id}/approve",
    response_model=ReturnResponse
)
def approve_return_api(
    return_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    try:
        return approve_return(
            db=db,
            return_id=return_id,
            admin_id=int(getattr(current_user, "id"))
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )