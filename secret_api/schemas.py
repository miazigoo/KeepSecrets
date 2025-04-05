from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class SecretInput(BaseModel):
    """Ввод секрета и время его хранения"""
    secret: str
    ttl_seconds: int


class KeyOutput(BaseModel):
    """Вывод ключа, нужного для раскодированния секрета"""
    key: str


class KeyInput(BaseModel):
    """Ввод ключа для раскодированния секрета"""
    key: str


class SecretOutput(BaseModel):
    """Вывод секрета"""
    secret: str


class LogOutput(BaseModel):
    """Вывод логов"""
    id: int
    timestamp: datetime
    status: str
    client_ip: Optional[str] = None
    details: Optional[str] = None
    ttl_seconds: Optional[int] = None