from passlib.context import CryptContext

from src.shared.configs.settings import settings

pwd_context = CryptContext(
    schemes=[settings.pwd_context_schemes], deprecated=settings.pwd_context_deprecated
)
