from sqlalchemy.orm import Session

from app.models.product import Product


def create_product(
    db: Session,
    name: str,
    sku: str,
    description: str | None,
    price
):
    product = Product(
        name=name,
        sku=sku,
        description=description,
        price=price
    )

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


def get_product_by_sku(
    db: Session,
    sku: str
):
    return (
        db.query(Product)
        .filter(Product.sku == sku)
        .first()
    )


def get_product_by_id(
    db: Session,
    product_id: int
):
    return (
        db.query(Product)
        .filter(Product.id == product_id)
        .first()
    )
    
def update_product(
    db: Session,
    product: Product,
    name: str | None,
    description: str | None,
    price
):
    if name is not None:
        setattr(product, "name", name)

    if description is not None:
        setattr(product, "description", description)

    if price is not None:
        setattr(product, "price", price)

    db.commit()
    db.refresh(product)

    return product

def activate_product(
    db: Session,
    product: Product
):
    setattr(product, "is_active", True)

    db.commit()
    db.refresh(product)

    return product
    
def deactivate_product(
    db:Session,
    product: Product
):
    setattr(product,"is_active", False)
    
    db.commit()
    db.refresh(product)
    
    return product

def get_all_products(
    db: Session
):
    return (
        db.query(Product)
        .order_by(Product.id.desc())
        .all()
    )