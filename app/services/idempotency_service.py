import hashlib
import json

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.idempotency import IdempotencyKey


def generate_request_hash(data: dict) -> str:
    request_string = json.dumps(
        data,
        sort_keys=True,
        default=str,
    )

    return hashlib.sha256(
        request_string.encode("utf-8")
    ).hexdigest()


def check_idempotency(
    db: Session,
    key: str,
    endpoint: str,
    user_id: int,
    request_hash: str,
):
    existing = (
        db.query(IdempotencyKey)
        .filter(
            IdempotencyKey.key == key,
            IdempotencyKey.endpoint == endpoint,
            IdempotencyKey.user_id == user_id,
        )
        .first()
    )

    if not existing:
        return None
    
    

    if str(existing.request_hash) != request_hash:
        raise HTTPException(
            status_code=409,
            detail="Idempotency key already used with different request data",
        )

    return existing


def save_idempotency_response(
    db: Session,
    key: str,
    endpoint: str,
    user_id: int,
    request_hash: str,
    response_status: int,
    response_body: dict,
):
    idempotency_record = IdempotencyKey(
        key=key,
        endpoint=endpoint,
        user_id=user_id,
        request_hash=request_hash,
        response_status=response_status,
        response_body=json.dumps(response_body, default=str),
    )

    db.add(idempotency_record)
    db.flush()

    return idempotency_record