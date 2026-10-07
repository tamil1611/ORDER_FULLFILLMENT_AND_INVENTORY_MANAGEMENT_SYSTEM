from sqlalchemy.orm import Session

from app.models.warehouse import Warehouse


def create_warehouse(
    db: Session,
    name: str,
    code: str,
    address: str
):
    warehouse = Warehouse(
        name=name,
        code=code,
        address=address
    )

    db.add(warehouse)
    db.commit()
    db.refresh(warehouse)

    return warehouse


def get_warehouse_by_code(
    db: Session,
    code: str
):
    return (
        db.query(Warehouse)
        .filter(Warehouse.code == code)
        .first()
    )


def get_warehouse_by_id(
    db: Session,
    warehouse_id: int
):
    return (
        db.query(Warehouse)
        .filter(Warehouse.id == warehouse_id)
        .first()
    )


def update_warehouse(
    db: Session,
    warehouse: Warehouse,
    name: str | None,
    address: str | None
):
    if name is not None:
        setattr(warehouse, "name", name)

    if address is not None:
        setattr(warehouse, "address", address)

    db.commit()
    db.refresh(warehouse)

    return warehouse


def deactivate_warehouse(
    db: Session,
    warehouse: Warehouse
):
    setattr(warehouse, "is_active", False)

    db.commit()
    db.refresh(warehouse)

    return warehouse


def activate_warehouse(
    db: Session,
    warehouse: Warehouse
):
    setattr(warehouse, "is_active", True)

    db.commit()
    db.refresh(warehouse)

    return warehouse


def get_all_warehouses(
    db: Session
):
    return (
        db.query(Warehouse)
        .order_by(Warehouse.id.desc())
        .all()
    )