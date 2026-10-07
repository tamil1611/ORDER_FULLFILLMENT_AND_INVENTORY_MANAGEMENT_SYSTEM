from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.dashboard_service import get_admin_dashboard, get_customer_dashboard, get_warehouse_manager_dashboard
from app.dependencies import require_role


router = APIRouter(
    prefix="/api/dashboard",
    tags=["Dashboard"]
)


@router.get("/admin")
def admin_dashboard(
    db: Session = Depends(get_db),
    current_user=Depends(require_role("admin"))
):
    return get_admin_dashboard(db)

@router.get("/warehouse/{warehouse_id}")
def warehouse_manager_dashboard(
    warehouse_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("warehouse_manager"))
):
    return get_warehouse_manager_dashboard(
        db=db,
        warehouse_id=warehouse_id
    )
    
@router.get("/customer/{customer_id}")
def customer_dashboard(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_role("customer"))
):
    return get_customer_dashboard(
        db=db,
        customer_id=customer_id
    )