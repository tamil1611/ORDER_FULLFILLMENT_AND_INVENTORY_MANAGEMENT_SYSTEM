from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import (
    create_user,
    get_user_by_email
    
)
from app.repositories.refresh_token_repository import(
    create_refresh_token as save_refresh_token
)
from app.auth import( 
                     hash_password, 
                     verify_password, 
                     create_access_token,
                     create_refresh_token as generate_refresh_token,
                     get_refresh_token_expiry)
from app.services.audit_log_service import log_action

def register_user(
    db: Session,
    name: str,
    email: str,
    password: str,
    role:str
):
    existing_user = get_user_by_email(db, email)

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(password)

    return create_user(
        db=db,
        name=name,
        email=email,
        hashed_password=hashed_password,
        role=role
    )


def login_user(
    db: Session,
    email: str,
    password: str
):
    user = get_user_by_email(db, email)

    if not user:
        log_action(
            db=db,
            user_id=None,
            action="FAILED_LOGIN",
            entity="User",
            entity_id=None,
            metadata={"email": email}
        )
        db.commit()

        raise ValueError("Invalid email or password")

    if not verify_password(password, str(user.password)):
        log_action(
            db=db,
            user_id=int(getattr(user,"id")),
            action="FAILED_LOGIN",
            entity="User",
            entity_id=int(getattr(user,"id")),
            metadata={"email": email}
        )
        db.commit()

        raise ValueError("Invalid email or password")

    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    refresh_token = generate_refresh_token(
        data={
            "sub": str(user.id),
            "role": user.role
        }
    )

    expires_at = get_refresh_token_expiry()

    save_refresh_token(
        db=db,
        user_id=int(getattr(user,"id")),
        token=refresh_token,
        expires_at=expires_at
    )

    log_action(
        db=db,
        user_id=int(getattr(user,"id")),
        action="LOGIN",
        entity="User",
        entity_id=int(getattr(user,"id")),
        metadata={"email": user.email}
    )

    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }
    

def change_password(
    db: Session,
    user: User,
    old_password: str,
    new_password: str
):
    # Check old password
    if not verify_password(
        old_password,
        str(user.password)
    ):
        raise ValueError("Old password is incorrect")

    # Hash new password
    new_hashed_password = hash_password(new_password)

    # Update password
    setattr(user,"password" ,new_hashed_password)

    db.commit()
    db.refresh(user)

    return user