import json

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse, PaymentConfirmRequest
from app.services import order_service as order_service
from app.dependencies import get_current_user
from fastapi import Header

from app.services.idempotency_service import check_idempotency, generate_request_hash, save_idempotency_response

router = APIRouter(
    prefix="/api/orders",
    tags=["Orders"]
)


@router.post("", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    idempotency_key: str = Header(..., alias="Idempotency-Key"),
):
    try:
        request_hash = generate_request_hash(
            order_data.model_dump()
        )

        existing = check_idempotency(
            db=db,
            key=idempotency_key,
            endpoint="/api/orders",
            user_id=current_user.id,
            request_hash=request_hash,
        )

        if existing is not None:
            response_body = str(existing.response_body)
            return json.loads(response_body)

        order = order_service.create_order(
            db=db,
            customer_id=current_user.id,
            order_data=order_data,
        )

        response = OrderResponse.model_validate(order)

        save_idempotency_response(
            db=db,
            key=idempotency_key,
            endpoint="/api/orders",
            user_id=current_user.id,
            request_hash=request_hash,
            response_status=201,
            response_body=response.model_dump(mode="json"),
        )

        db.commit()

        return response

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e),
        )

@router.get(
    "",
    response_model=list[OrderResponse]
)
def get_customer_orders(
    page: int = 1,
    page_size: int = 20,
    status: str|None=None,
    warehouse_id:int |None=None,
    payment_status:str|None=None,
    min_total_amount: float | None = None,
    max_total_amount: float | None = None,
    customer_id:int|None=None,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return order_service.get_customer_orders(
        db=db,
        customer_id=current_user.id,
        page=page,
        page_size=page_size,
        status=status,
        
        
    )


@router.get(
    "/{order_id}",
    response_model=OrderResponse
)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    order = order_service.get_order(
        db=db,
        order_id=order_id
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    if order.customer_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view this order"
        )

    return order

@router.post(
    "/{order_id}/payment-confirm",
    response_model=OrderResponse
)
def confirm_payment(
    order_id: int,
    payment_data: PaymentConfirmRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    idempotency_key: str = Header(
        ...,
        alias="Idempotency-Key"
    ),
):
    try:
        request_hash = generate_request_hash(
            payment_data.model_dump()
        )

        existing = check_idempotency(
            db=db,
            key=idempotency_key,
            endpoint=f"/api/orders/{order_id}/payment-confirm",
            user_id=current_user.id,
            request_hash=request_hash,
        )

        if existing is not None:
            response_body = str(existing.response_body)
            return json.loads(response_body)

        order = order_service.confirm_payment(
            db=db,
            order_id=order_id,
            payment_reference=payment_data.payment_reference,
            user_id=current_user.id,
        )

        response = OrderResponse.model_validate(order)

        save_idempotency_response(
            db=db,
            key=idempotency_key,
            endpoint=f"/api/orders/{order_id}/payment-confirm",
            user_id=current_user.id,
            request_hash=request_hash,
            response_status=200,
            response_body=response.model_dump(mode="json"),
        )

        db.commit()

        return response

    except ValueError as e:
        db.rollback()

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/{order_id}/confirm",
    response_model=OrderResponse
)
def confirm_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.confirm_order(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/{order_id}/fulfill",
    response_model=OrderResponse
)
def fulfill_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.fulfill_order(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )  
        
@router.post(
    "/{order_id}/ship",
    response_model=OrderResponse
)
def ship_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.ship_order(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.post(
    "/{order_id}/deliver",
    response_model=OrderResponse
)
def deliver_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.deliver_order(
            db=db,
            order_id=order_id,
            user_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
              

@router.post(
    "/{order_id}/return",
    response_model=OrderResponse
)
def return_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.return_order(
            db=db,
            order_id=order_id,
            customer_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post(
    "/{order_id}/cancel",
    response_model=OrderResponse
)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.cancel_order(
            db=db,
            order_id=order_id,
            customer_id=current_user.id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )
        
@router.patch("/{order_id}/assign")
def assign_order(
    order_id: int,
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    try:
        return order_service.assign_order(
            db=db,
            order_id=order_id,
            warehouse_id=warehouse_id
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )