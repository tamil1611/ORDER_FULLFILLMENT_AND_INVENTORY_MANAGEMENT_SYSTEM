from sqlalchemy.orm import Session

from app.models.notification import Notification
from app.repositories.notification_repository import (
    get_notifications,
    get_notification_by_id,
    mark_as_read,
    mark_all_as_read,
)


def get_user_notifications(
    db: Session,
    user_id: int
):
    return get_notifications(
        db=db,
        user_id=user_id
    )


def read_notification(
    db: Session,
    notification_id: int,
    user_id: int
):
    notification = get_notification_by_id(
        db=db,
        notification_id=notification_id,
        user_id=user_id
    )

    if not notification:
        return None

    return mark_as_read(
        db=db,
        notification=notification
    )


def read_all_notifications(
    db: Session,
    user_id: int
):
    return mark_all_as_read(
        db=db,
        user_id=user_id
    )


def create_notification(
    db: Session,
    user_id: int,
    title: str,
    message: str,
    notification_type: str
):
    notification = Notification(
        user_id=user_id,
        title=title,
        message=message,
        notification_type=notification_type,
        is_read=False
    )

    db.add(notification)
    db.commit()
    db.refresh(notification)

    return notification