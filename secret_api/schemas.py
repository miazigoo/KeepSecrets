from pydantic import BaseModel


class SecretInput(BaseModel):
    secret: str


class KeyOutput(BaseModel):
    key: str