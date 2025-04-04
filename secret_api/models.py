from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


Base = declarative_base()


class Secret(Base):
    __tablename__ = 'secret'
    id = Column(Integer, primary_key=True)
    secret = Column(String, nullable=False)
    secret_key = Column(String, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())