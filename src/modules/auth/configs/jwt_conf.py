import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_EXPIRE_MIN = os.getenv("ACCESS_EXPIRE_MIN", 150000)
REFRESH_EXPIRE_DAYS = os.getenv("REFRESH_EXPIRE_DAYS", 7)
