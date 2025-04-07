from environs import Env
from sqlalchemy import  create_engine
from sqlalchemy.orm import sessionmaker

from secret_api.models import Base


env = Env()
env.read_env()

POSTGRES_USER = env.str("POSTGRES_USER")
POSTGRES_PASSWORD = env.str("POSTGRES_PASSWORD")
POSTGRES_HOST = env.str("POSTGRES_HOST")
POSTGRES_PORT = env.int("POSTGRES_PORT")
POSTGRES_DB = env.str("POSTGRES_DB")

POSTGRESQL_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

engine = create_engine(
    POSTGRESQL_URL)


new_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)

Base.metadata.create_all(bind=engine)


async def get_db():
    db = new_session()
    try:
        yield db
    finally:
        db.close()
