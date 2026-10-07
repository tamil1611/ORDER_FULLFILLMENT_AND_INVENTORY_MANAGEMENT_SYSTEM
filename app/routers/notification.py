from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.notification import NotificationResponse
from app.services.notification_service import (
    get_user_notifications,
    read_notification,
    read_all_notifications,
)
from app.dependencies import get_current_user


router = APIRouter(
    prefix="/api/notifications",
    tags=["Notifications"]
)


@router.get(
    "",
    response_model=list[NotificationResponse]
)
def get_notifications(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return get_user_notifications(
        db=db,
        user_id=current_user.id
    )


@router.patch(
    "/{notification_id}/read",
    response_model=NotificationResponse
)
def mark_notification_as_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    notification = read_notification(
        db=db,
        notification_id=notification_id,
        user_id=current_user.id
    )

    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Notification not found"
        )

    return notification


@router.patch(
    "/read-all",
    response_model=list[NotificationResponse]
)
def mark_all_notifications_as_read(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    return read_all_notifications(
        db=db,
        user_id=current_user.id
    )