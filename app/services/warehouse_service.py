from sqlalchemy.orm import Session

from app.repositories.warehouse_repository import (
    create_warehouse,
    get_warehouse_by_code,
    get_warehouse_by_id,
    update_warehouse,
    deactivate_warehouse,
    activate_warehouse,
    get_all_warehouses
)


def create_new_warehouse(
    db: Session,
    name: str,
    code: str,
    address: str
):
    existing_warehouse = get_warehouse_by_code(
        db=db,
        code=code
    )

    if existing_warehouse:
        raise ValueError("Warehouse code already exists")

    return create_warehouse(
        db=db,
        name=name,
        code=code,
        address=address
    )


def get_warehouse(
    db: Session,
    warehouse_id: int
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    return warehouse


def update_existing_warehouse(
    db: Session,
    warehouse_id: int,
    name: str | None,
    address: str | None
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    return update_warehouse(
        db=db,
        warehouse=warehouse,
        name=name,
        address=address
    )


def deactivate_existing_warehouse(
    db: Session,
    warehouse_id: int
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    if not bool(warehouse.is_active):
        raise ValueError("Warehouse already inactive")

    return deactivate_warehouse(
        db=db,
        warehouse=warehouse
    )


def activate_existing_warehouse(
    db: Session,
    warehouse_id: int
):
    warehouse = get_warehouse_by_id(
        db=db,
        warehouse_id=warehouse_id
    )

    if not warehouse:
        raise ValueError("Warehouse not found")

    if bool(warehouse.is_active):
        raise ValueError("Warehouse already active")

    return activate_warehouse(
        db=db,
        warehouse=warehouse
    )


def get_warehouses(
    db: Session
):
    return get_all_warehouses(db=db)