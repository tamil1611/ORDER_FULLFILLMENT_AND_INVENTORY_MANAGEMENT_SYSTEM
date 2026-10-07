from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.auth import (create_access_token, 
                      decode_refresh_token,
                      create_refresh_token,
                      get_refresh_token_expiry)
from app.database import get_db
from app.dependencies import get_current_user
from app.models.user import User
from app.repositories.refresh_token_repository import (
    get_refresh_token,
    revoke_refresh_token,
    create_refresh_token as save_refresh_token)
from app.schemas.user import ChangePassword, UserCreate, UserLogin,UserResponse
from app.services.auth_service import change_password, register_user, login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db)
):
    try:
        return register_user(
            db=db,
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            role=user_data.role
        )

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login")
def login(
    user_data:OAuth2PasswordRequestForm=Depends(),
    db: Session = Depends(get_db)
):
    try:
        tokens = login_user(
            db=db,
            email=user_data.username,
            password=user_data.password
        )

        return {
            "access_token": tokens["access_token"],
            "refresh_token":tokens["refresh_token"],
            "token_type": "bearer"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
        
@router.get("/me", response_model=UserResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    return current_user



@router.post("/refresh")
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    payload = decode_refresh_token(refresh_token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    token_record = get_refresh_token(
        db=db,
        token=refresh_token
    )

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token not found"
        )

    if bool(token_record.is_revoked):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has been revoked"
        )
        
    user = db.query(User).filter(
    User.id == int(payload["sub"])
    ).first()

    if not user:
      raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="User not found"
    )

    if not bool(user.is_active):
       raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="User is inactive"
    )

    # Revoke old refresh token
    revoke_refresh_token(
        db=db,
        token_record=token_record
    )

    # Create new access token
    new_access_token = create_access_token(
        data={
            "sub": payload["sub"],
            "role": payload["role"]
        }
    )

    # Create new refresh token
    new_refresh_token = create_refresh_token(
        data={
            "sub": payload["sub"],
            "role": payload["role"]
        }
    )

    # Save new refresh token
    save_refresh_token(
        db=db,
        user_id=int(payload["sub"]),
        token=new_refresh_token,
        expires_at=get_refresh_token_expiry()
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }
    
@router.post("/logout")
def logout(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    token_record = get_refresh_token(
        db=db,
        token=refresh_token
    )

    if not token_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Refresh token not found"
        )

    if bool(token_record.is_revoked):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Refresh token already revoked"
        )

    revoke_refresh_token(
        db=db,
        token_record=token_record
    )

    return {
        "message": "Logout successful"
    }
    

@router.post("/change-password")
def change_user_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    try:
        change_password(
            db=db,
            user=current_user,
            old_password=password_data.old_password,
            new_password=password_data.new_password
        )

        return {
            "message": "Password changed successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )