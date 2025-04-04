from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import engine, new_session
from secret_api.cryptography import generate_key, encrypt_secret
from secret_api.models import Base, Secret
from secret_api.schemas import KeyOutput, SecretInput

router = APIRouter()

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_secret", response_model=KeyOutput)
async def keep_secret(
        secret_in: SecretInput, db: Session = Depends(get_db)
):
    secret = secret_in.secret
    key = generate_key()
    encrypted_secret = encrypt_secret(secret, key)
    new_secret = Secret(secret=encrypted_secret, secret_key=key)
    db.add(new_secret)
    db.commit()
    return KeyOutput(key=key)


@router.get("/wallet_info/default")
async def list_secret(
        db: Session = Depends(get_db)
):
    """
    Получение списка секретов
    """
    secrets = db.query(Secret).order_by(Secret.created_at).all()
    return secrets
