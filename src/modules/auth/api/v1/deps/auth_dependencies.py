from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError

from src.modules.auth.api.v1.services.jwt_service import decode_token

token_scheme = HTTPBearer()


async def authenticate_user(credentials: HTTPAuthorizationCredentials = Depends(token_scheme)):
    token = credentials.credentials
    try:
        return decode_token(token)
    except JWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token: {str(exc)}"
        )


async def verify_superuser(payload: dict = Depends(authenticate_user)):
    if not payload.get("is_superuser"):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User is not a superuser"
        )
    return payload
