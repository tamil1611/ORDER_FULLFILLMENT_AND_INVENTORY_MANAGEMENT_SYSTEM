from sqlalchemy.orm import Session

from app.models.notification import Notification


def get_notifications(
    db: Session,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )


def get_notification_by_id(
    db: Session,
    notification_id: int,
    user_id: int
):
    return (
        db.query(Notification)
        .filter(
            Notification.id == notification_id,
            Notification.user_id == user_id
        )
        .first()
    )


def mark_as_read(
    db: Session,
    notification: Notification
):
    setattr(notification,"is_read" , True)

    db.commit()
    db.refresh(notification)

    return notification


def mark_all_as_read(
    db: Session,
    user_id: int
):
    notifications = (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read.is_(False)
        )
        .all()
    )

    for notification in notifications:
        setattr(notification,"is_read" , True)

    db.commit()

    return (
        db.query(Notification)
        .filter(Notification.user_id==user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )