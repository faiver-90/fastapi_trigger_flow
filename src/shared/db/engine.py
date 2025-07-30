import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
user = os.getenv("POSTGRES_USER", "pgres")
pw = os.getenv("POSTGRES_PASSWORD", "pgres")
port = os.getenv("POSTGRES_PORT", 5432)
db_name = os.getenv("POSTGRES_DB", "pgres")
host = os.getenv("POSTGRES_HOST", "db")
SYNC_DATABASE_URL = os.getenv("SYNC_DATABASE_URL")
DATABASE_URL = f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}"

async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    future=True,
    pool_size=20,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,
)
sync_engine = create_engine(SYNC_DATABASE_URL, echo=True)
