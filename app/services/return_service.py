from sqlalchemy.orm import Session

from app.models.return_models import Return
from app.repositories import return_repository
from app.repositories.order_repository import get_order_by_id
from app.services.audit_log_service import log_action


def create_return_request(
    db: Session,
    order_id: int,
    customer_id: int,
    reason: str
):
    order = get_order_by_id(
        db,
        order_id
    )

    if not order:
        raise ValueError("Order not found")

    if order.customer_id != customer_id:
        raise ValueError(
            "You are not allowed to return this order"
        )

    if order.status != "DELIVERED":
        raise ValueError(
            "Only delivered orders can be returned"
        )

    return_request = Return(
        order_id=order_id,
        customer_id=customer_id,
        reason=reason,
        status="REQUESTED"
    )

    return_repository.create_return(
        db,
        return_request
    )

    log_action(
        db=db,
        user_id=customer_id,
        action="RETURN_CREATED",
        entity="Return",
        entity_id=getattr(return_request, "id"),
        metadata={
            "order_id": order_id,
            "reason": reason,
            "status": "REQUESTED"
        }
    )

    db.commit()
    db.refresh(return_request)

    return return_request

def approve_return(
    db: Session,
    return_id: int,
    admin_id: int
):
    return_request = return_repository.get_return_by_id(
        db,
        return_id
    )

    if not return_request:
        raise ValueError("Return not found")

    if return_request.status != "REQUESTED":
        raise ValueError(
            "Only requested returns can be approved"
        )

    return_request.status = "APPROVED"

    log_action(
        db=db,
        user_id=admin_id,
        action="RETURN_APPROVED",
        entity="Return",
        entity_id=getattr(return_request, "id"),
        metadata={
            "order_id": return_request.order_id,
            "customer_id": return_request.customer_id
        }
    )

    db.commit()
    db.refresh(return_request)

    return return_request