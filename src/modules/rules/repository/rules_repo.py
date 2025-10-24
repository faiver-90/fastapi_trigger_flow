import asyncio

from pydantic import BaseModel
from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.shared.base_repo import BaseRepository
from src.shared.db import Notifications, Rules, Sources, Triggers, User
from src.shared.db.session import AsyncSessionLocal


class RulesCreateSchema(BaseModel):
    user_id: int | None
    source_id: int | None
    trigger_id: int | None
    user_notification_ids: list[int] | None
    is_active: bool | None = True


class RulesRepo(BaseRepository[Rules]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Rules)

    async def parce_rules(self) -> list[RulesCreateSchema]:
        """
        Collect field to rules

        select u.id as user_id, s.id as source_id, t.id as trigger_id, n.id as notification_id
        from public.users as u left join public.sources as s on u.id = s.user_id and s.is_active is True
        left join public.triggers as t on u.id = t.user_id and t.is_active is True
        left join public.notifications as n on u.id = n.user_id and n.is_active is True
        where s.is_active is True and n.is_active is True and t.is_active is True;
        """
        stmt = (
            select(
                User.id.label("user_id"),
                Sources.id.label("source_id"),
                Triggers.id.label("trigger_id"),
                func.array_agg(Notifications.id).label("user_notification_ids"),
                # опционально статус правила:
                # func.bool_and(Notifications.is_active).label("is_active")
            )
            .join(
                Sources, and_(User.id == Sources.user_id, Sources.is_active.is_(True))
            )
            .join(
                Triggers,
                and_(User.id == Triggers.user_id, Triggers.is_active.is_(True)),
            )
            .join(
                Notifications,
                and_(
                    User.id == Notifications.user_id, Notifications.is_active.is_(True)
                ),
            )
            .group_by(User.id, Sources.id, Triggers.id)
        )
        result = await self.session.execute(stmt)
        rows = result.mappings().all()
        return [RulesCreateSchema(**row) for row in rows]


async def main():
    async with AsyncSessionLocal() as session:
        repo = RulesRepo(session)
        result = await repo.parce_rules()
        print(result)
        await repo.create_many(result)


if __name__ == "__main__":
    asyncio.run(main())
