from sqlalchemy.orm import Session

from app.models.product import Product
from app.models.user import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    name: str,
    email: str,
    hashed_password: str,
    role: str = "customer"
):
    user = User(
        name=name,
        email=email,
        password=hashed_password,
        role=role
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

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