import os

from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine

load_dotenv()
user = os.getenv('POSTGRES_USER', 'pgres')
pw = os.getenv('POSTGRES_PASSWORD', 'pgres')
port = os.getenv('POSTGRES_PORT', 5432)
db_name = os.getenv('POSTGRES_DB', 'pgres')
host = os.getenv('POSTGRES_HOST', 'db')
DATABASE_URL = f"postgresql+asyncpg://{user}:{pw}@{host}:{port}/{db_name}"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)
