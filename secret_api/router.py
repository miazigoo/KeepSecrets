from contextlib import contextmanager

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import engine, new_session
from redis_db import get_redis_connection
from secret_api.cryptography import generate_key, encrypt_secret, decrypt_secret, store_secret_in_redis, \
    read_secret_from_redis, delete_secret_from_redis
from secret_api.models import Base, Secret
from secret_api.schemas import KeyOutput, SecretInput, SecretOutput, KeyInput

router = APIRouter()

Base.metadata.create_all(bind=engine)


@contextmanager
async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()


@router.post("/add_secret", response_model=KeyOutput)
async def keep_secret(
        secret_in: SecretInput, redis_conn=Depends(get_redis_connection)
):
    """Добавление секрета в БД и вывод ключа для раскодировки"""
    secret = secret_in.secret
    key = generate_key()
    encrypted_secret = encrypt_secret(secret, key)
    store_secret_in_redis(key, encrypted_secret)
    return KeyOutput(key=key)


@router.post("/get_secret", response_model=SecretOutput)
async def keep_secret(
        key_in: KeyInput, db: Session = Depends(get_db)
):
    """Получение раскодированного секрета из БД и его удаление"""
    key = key_in.key
    encrypted_secret = read_secret_from_redis(key)
    if encrypted_secret is None:
        raise HTTPException(status_code=404, detail="Secret not found")
    decrypt_secrets = decrypt_secret(encrypted_secret, key)
    delete_secret_from_redis(key)
    secret_status = "Секрет удален"

    return SecretOutput(secret=decrypt_secrets, status=secret_status)

