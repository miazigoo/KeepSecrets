from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

class Logs(Base):
    """Модель логов"""
    __tablename__ = 'logs'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)
    client_ip = Column(String)
    details = Column(String)
    ttl_seconds = Column(Integer, nullable=True)