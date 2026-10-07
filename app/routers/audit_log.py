from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import require_role
from app.schemas.audit_log import AuditLogResponse
from app.services.audit_log_service import list_audit_logs


router = APIRouter(
    prefix="/api/audit-logs",
    tags=["Audit Logs"]
)


@router.get(
    "",
    response_model=list[AuditLogResponse]
)
def get_audit_logs_list(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return list_audit_logs(
        db=db,
        skip=skip,
        limit=limit
    )