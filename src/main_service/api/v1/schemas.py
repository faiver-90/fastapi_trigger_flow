from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class JWTCreateSchema(BaseModel):
    user_id: int
    token: str


class AuthInSchema(BaseModel):
    password: str
    username: str
    chat_id: str


class AuthOutSchema(BaseModel):
    access_token: str
    refresh_token: str


class UserCreateSchema(BaseModel):
    username: str = Field(min_length=3, max_length=150)
    email: EmailStr
    password: str = Field(min_length=6)


class UserOutSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_superuser: bool

    class Config:
        from_attributes = True


class TokenResponseSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_at: datetime
    user: UserOutSchema
