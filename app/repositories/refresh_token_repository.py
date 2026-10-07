from datetime import datetime

from sqlalchemy.orm import Session

from app.models.refresh_token import RefreshToken


def create_refresh_token(
    db: Session,
    user_id: int,
    token: str,
    expires_at: datetime
):
    refresh_token = RefreshToken(
        user_id=user_id,
        token=token,
        expires_at=expires_at
    )

    db.add(refresh_token)
    db.commit()
    db.refresh(refresh_token)

    return refresh_token

def get_refresh_token(
    db:Session,
    token:str
):
    return(
        db.query(RefreshToken)
        .filter(RefreshToken.token==token)
        .first()
    )
    
def revoke_refresh_token(
    db: Session,
    token_record: RefreshToken
):
    setattr(token_record,"is_revoked" , True)

    db.commit()
    db.refresh(token_record)

    return token_record