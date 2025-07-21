from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, exists, or_

from src.modules.auth.api.v1.schemas import UserCreateSchema
from src.shared.db.models.auth import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_fields(self, **kwargs) -> User | None:
        conditions = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                conditions.append(getattr(User, key) == value)
            else:
                raise ValueError(f"Invalid field: {key}")

        stmt = select(User).where(and_(*conditions))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def exists_by_fields(self, **kwargs) -> bool:
        conditions = []
        for key, value in kwargs.items():
            if hasattr(User, key):
                conditions.append(getattr(User, key) == value)
            else:
                raise ValueError(f"Invalid field: {key}")

        stmt = select(exists().where(or_(*conditions)))
        result = await self.session.execute(stmt)
        return result.scalar()

    # async def update_user_by_id(self, user_id: int, data: dict) -> Optional[User]:
    #     await self.session.execute(
    #         update(User).where(User.id == user_id).values(**data)
    #     )
    #     await self.session.commit()
    #     return await self.get_by_fields(id=user_id)

    async def create(self, user_data: UserCreateSchema, hashed_password: str) -> User:
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
