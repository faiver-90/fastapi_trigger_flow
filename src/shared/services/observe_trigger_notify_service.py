from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from collections import defaultdict

from src.shared.db import UserTriggerBinding, UserNotificationBinding
from src.modules.api_source.api.v1.trigger.trigger_registry import TRIGGER_REGISTRY
from src.modules.api_source.api.v1.notifications.notifications_registry import NOTIFY_REGISTRY

from sqlalchemy import select
from collections import defaultdict


class TriggerExecutorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def run_for_all_sources(self, payloads: dict[int, dict]):
        """
        payloads: {data_source_id: payload}
        """
        stmt = (
            select(UserTriggerBinding, UserNotificationBinding)
            .join(UserNotificationBinding, UserNotificationBinding.user_trigger_id == UserTriggerBinding.id)
            .where(UserTriggerBinding.data_source_id.in_(payloads.keys()))
        )
        result = await self.session.execute(stmt)
        rows = result.all()

        trigger_map: dict[int, list[tuple[UserTriggerBinding, UserNotificationBinding]]] = defaultdict(list)
        for trigger, notification in rows:
            trigger_map[trigger.data_source_id].append((trigger, notification))

        for data_source_id, trigger_items in trigger_map.items():
            payload = payloads.get(data_source_id)
            if not payload:
                continue

            # группируем триггеры
            grouped_triggers = defaultdict(list)
            for trigger, notif in trigger_items:
                grouped_triggers[trigger].append(notif)

            for trigger, notifs in grouped_triggers.items():
                trigger_func = TRIGGER_REGISTRY.get(trigger.trigger_type)
                if not trigger_func:
                    continue
                try:
                    if trigger_func(payload, trigger.trigger_params):
                        await self._notify(notifs, payload)
                except Exception as e:
                    print(f"[!] Trigger error: {e}")

    async def _notify(self, notifications: list[UserNotificationBinding], payload: dict):
        for notif in notifications:
            for notif_type in notif.notification_type:
                notifier = NOTIFY_REGISTRY.get(notif_type)
                if not notifier:
                    continue
                try:
                    await notifier.send(payload, notif.notification_config or {})
                except Exception as e:
                    print(f"[!] Notification error: {e}")


p = {
    "data_source_id": 1,
    "user_id": 1,
    "triggers": [
        {
            "trigger_type": "temp_trigger",
            "trigger_params": {
                "temp": "1",
                "op": ">"
            },
            "notifications": [
                {
                    "notification_type": [
                        "console"
                    ],
                    "notification_config": {
                        "additionalProp1": {}
                    }
                }
            ]
        },
        {
            "trigger_type": "temp_trigger",
            "trigger_params": {
                "trigger_params": {
                    "temp": "1",
                    "op": ">"
                }
            },
            "notifications": [
                {
                    "notification_type": [
                        "console"
                    ],
                    "notification_config": {
                        "additionalProp1": {}
                    }
                }
            ]
        },
    ]
}
