from datetime import timedelta, datetime

from sqlalchemy.ext.asyncio import AsyncSession

from api.v1.configs.jwt_conf import REFRESH_EXPIRE_DAYS
from api.v1.schemas import JWTCreateSchema
from db.models import RefreshToken


class JWTRepo:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self,
                     jwt_data: JWTCreateSchema):
        expires_at = datetime.utcnow() + timedelta(days=REFRESH_EXPIRE_DAYS)

        jwt = RefreshToken(
            user_id=jwt_data.user_id,
            token=jwt_data.token,
            expires_at=expires_at,
            revoked=False
        )
        self.session.add(jwt)
        await self.session.commit()
        await self.session.refresh(jwt)
        return jwt
