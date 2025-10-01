import os

from dotenv import load_dotenv
from passlib.context import CryptContext

load_dotenv()

PWD_CONTEXT_SCHEMES = os.getenv("PWD_CONTEXT_SCHEMES", "bcrypt")
PWD_CONTEXT_DEPRECATED = os.getenv("PWD_CONTEXT_DEPRECATED", "auto")

pwd_context = CryptContext(
    schemes=[PWD_CONTEXT_SCHEMES], deprecated=PWD_CONTEXT_DEPRECATED
)
