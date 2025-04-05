from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from database import get_db
from secret_api.cryptography import generate_key, encrypt_secret, decrypt_secret, store_secret_in_redis, \
    read_secret_from_redis, delete_secret_from_redis
from secret_api.models import Logs
from secret_api.schemas import KeyOutput, SecretInput, SecretOutput, LogOutput

router = APIRouter()


@router.post("/add_secret", response_model=KeyOutput)
async def keep_secret(
        secret_in: SecretInput,
        request: Request,
        db: Session = Depends(get_db)
):
    """
    Добавление секрета в БД и вывод ключа для раскодировки.
    Пример тела запроса:
    {
      "secret": "доступ к конфиденциальным данным",
      "ttl_seconds": 300
    }
    Пример ответа (JSON):
    {"key": "уникальный идентификатор"}
    """
    secret = secret_in.secret
    ttl_seconds = secret_in.ttl_seconds
    if ttl_seconds == 0:
        ttl_seconds += 3600
    key = generate_key()
    encrypted_secret = encrypt_secret(secret, key)
    store_secret_in_redis(key, encrypted_secret, ttl_seconds)

    # Логи на создание секрета
    log = Logs(
        timestamp=datetime.now(),
        status="CREATE_SECRET",
        client_ip=request.client.host,
        ttl_seconds=ttl_seconds,
        details=f"Created secret with key {key} And ttl_seconds = {ttl_seconds}"
    )
    db.add(log)
    db.commit()
    return KeyOutput(key=key)


@router.get("/get_secret/{key}", response_model=SecretOutput)
async def view_secret(
        key: str, request: Request,
        db: Session = Depends(get_db)
):
    """
    Получение раскодированного секрета из БД и его удаление:
    {"secret": "доступ к конфиденциальным данным"}
    """
    encrypted_secret = read_secret_from_redis(key)
    if encrypted_secret is None:
        return JSONResponse(status_code=404, content={'message': 'Secret not found'})
    decrypt_secrets = decrypt_secret(encrypted_secret, key)

    # Логи на чтение секрета
    log = Logs(
        timestamp=datetime.now(),
        status="READ_SECRET",
        client_ip=request.client.host,
        details=f"Read secret with key {key}"
    )
    db.add(log)
    db.commit()

    delete_secret_from_redis(key)
    # Логи на удаление секрета
    log = Logs(
        timestamp=datetime.now(),
        status="DELETE_SECRET",
        client_ip=request.client.host,
        details=f"Delete secret with key {key}"
    )
    db.add(log)
    db.commit()

    return SecretOutput(secret=decrypt_secrets)


@router.delete("/delete_secrets/{key}")
async def delete_secret(
        key: str, request: Request,
        db: Session = Depends(get_db)
):
    """
    Удаление секрета
    Пример ответа (JSON):
    {
      "status": "secret_deleted"
    }
    """
    encrypted_secret = read_secret_from_redis(key)

    if not encrypted_secret:
        return JSONResponse(status_code=404, content={'status': 'Secret not found'})

    delete_secret_from_redis(key)

    # Логи на удаление секрета
    log = Logs(
        timestamp=datetime.now(),
        status="DELETE_SECRET",
        client_ip=request.client.host,
        details=f"Delete secret with key {key}"
    )
    db.add(log)
    db.commit()

    return JSONResponse(content={'status': 'secret_deleted'}, status_code=200)


@router.get("/logs", response_model=List[LogOutput])
async def get_logs(db: Session = Depends(get_db)):
    """Вывод логов из БД"""
    logs = db.query(Logs).order_by(Logs.timestamp.desc()).all()
    return logs
