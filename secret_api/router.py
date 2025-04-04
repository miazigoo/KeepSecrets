from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, new_session
from secret_api.cryptography import generate_key, encrypt_secret, decrypt_secret
from secret_api.models import Base, Secret
from secret_api.schemas import KeyOutput, SecretInput, SecretOutput, KeyInput

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
    """Добавление секрета в БД и вывод ключа для раскодировки"""
    secret = secret_in.secret
    key = generate_key()
    encrypted_secret = encrypt_secret(secret, key)
    new_secret = Secret(secret=encrypted_secret, secret_key=key)
    db.add(new_secret)
    db.commit()
    return KeyOutput(key=key)


@router.post("/get_secret", response_model=SecretOutput)
async def keep_secret(
        key_in: KeyInput, db: Session = Depends(get_db)
):
    """Получение раскодированного секрета из БД и его удаление"""
    key = key_in.key
    encrypted_secret = db.query(Secret).filter(Secret.secret_key == key).first()
    if encrypted_secret is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    decrypt_secrets = decrypt_secret(encrypted_secret.secret, key)
    db.delete(encrypted_secret)
    db.commit()
    secret_status = "Секрет удален"

    return SecretOutput(secret=decrypt_secrets, status=secret_status)


@router.get("/wallet_info/default")
async def list_secret(
        db: Session = Depends(get_db)
):
    """
    Получение списка секретов
    """
    secrets = db.query(Secret).order_by(Secret.created_at).all()
    return secrets
