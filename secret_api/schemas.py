from pydantic import BaseModel


class SecretInput(BaseModel):
    secret: str


class KeyOutput(BaseModel):
    key: str


class KeyInput(BaseModel):
    key: str


class SecretOutput(BaseModel):
    secret: str
    status: str