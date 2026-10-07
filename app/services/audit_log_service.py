from sqlalchemy.orm import Session

from app.repositories.audit_log_repository import create_audit_log, get_audit_logs


def log_action(
    db: Session,
    user_id: int | None,
    action: str,
    entity: str,
    entity_id: int | None = None,
    ip_address: str | None = None,
    metadata: dict | None = None
):
    return create_audit_log(
        db=db,
        user_id=user_id,
        action=action,
        entity=entity,
        entity_id=entity_id,
        ip_address=ip_address,
        metadata=metadata
    )
    
def list_audit_logs(
    db: Session,
    skip: int = 0,
    limit: int = 100
):
    return get_audit_logs(
        db=db,
        skip=skip,
        limit=limit
    )