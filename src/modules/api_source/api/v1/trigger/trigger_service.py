from src.modules.api_source.api.v1.notifications.notification_repo import NotificationRepo
from src.modules.api_source.api.v1.trigger.trigger_repo import TriggerRepo
from src.modules.api_source.api.v1.trigger.trigger_schemas import BulkTriggerCreate
from src.shared.db import UserTriggerBinding, UserNotificationBinding
from src.shared.services.base_crud_service import BaseCRUDService


class TriggerService(BaseCRUDService[TriggerRepo]):
    def __init__(self, repo: TriggerRepo, notification_repo: NotificationRepo):
        super().__init__(repo)
        self.notification_repo = notification_repo

    async def bulk_create(self, data: BulkTriggerCreate):
        async with self.repo.session.begin():
            triggers = self._build_triggers(data)
            self.repo.session.add_all(triggers)
            await self.repo.session.flush()

            notifications = self._build_notifications(triggers, data)
            await self.notification_repo.add_all(notifications)

        return {
            "created_triggers": len(triggers),
            "created_notifications": len(notifications)
        }

    @staticmethod
    def _build_triggers(data: BulkTriggerCreate) -> list[UserTriggerBinding]:
        return [
            UserTriggerBinding(**t.model_dump(exclude={"notifications"}), user_id=data.user_id, data_source_id=data.data_source_id)
            for t in data.triggers
        ]

    @staticmethod
    def _build_notifications(triggers: list[UserTriggerBinding], data: BulkTriggerCreate) \
            -> list[UserNotificationBinding]:
        notifications: list[UserNotificationBinding] = []

        for trigger, trigger_data in zip(triggers, data.triggers):
            for notif in trigger_data.notifications:
                notif_data = notif.model_dump()
                notifications.append(UserNotificationBinding(user_trigger_id=trigger.id, **notif_data))
        return notifications
