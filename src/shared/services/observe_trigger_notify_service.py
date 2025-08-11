from collections import defaultdict

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.modules.api_source.api.v1.trigger.trigger_registry import TRIGGER_REGISTRY
from src.shared.celery_module.tasks import notify_email, notify_sms, notify_tg
from src.shared.db import UserNotificationBinding, UserTriggerBinding


class TriggerExecutorService:
    """
    Сервис для обработки пользовательских триггеров и отправки уведомлений на основе входящих данных от внешних
    источников (payloads).

    Основная задача сервиса — найти все активные триггеры, связанные с указанными источниками данных (data_source_id),
    проверить выполнение условий триггеров на входящих данных и при срабатывании триггера инициировать соответствующие
     уведомления.

    Атрибуты:
        session (AsyncSession): асинхронная сессия SQLAlchemy для доступа к базе данных.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def run_for_all_sources(self, payloads: dict[int, dict]):
        """
        Запускает обработку для всех указанных источников данных.

        Args:
            payloads (dict[int, dict]): словарь вида {data_source_id: payload}, где payload — входные данные,
                поступившие от соответствующего внешнего API.

        Пропускает источники, по которым отсутствуют триггеры, или для которых не передан payload.
        """
        rows = await self._load_triggers_with_notifications(payloads)
        grouped_by_source = self._group_by_data_source(rows)

        for data_source_id, trigger_items in grouped_by_source.items():
            payload = payloads.get(data_source_id)
            if not payload:
                continue
            await self._run_for_one_source(trigger_items, payload)

    async def _load_triggers_with_notifications(self, payloads: dict[int, dict]):
        """
        Выполняет SQL-запрос, объединяющий триггеры и связанные с ними уведомления для всех указанных источников.

        Args:
            payloads (dict[int, dict]): карта источников и данных.

        Returns:
            list[tuple[UserTriggerBinding, UserNotificationBinding]]: результат запроса.
        """
        # TODO Перенести в REPO
        stmt = (
            select(UserTriggerBinding, UserNotificationBinding)
            .join(
                UserNotificationBinding,
                UserNotificationBinding.user_trigger_id == UserTriggerBinding.id,
            )
            .where(UserTriggerBinding.data_source_id.in_(payloads.keys()))
        )
        result = await self.session.execute(stmt)
        return result.all()

    @staticmethod
    def _group_by_data_source(
        rows: list[tuple[UserTriggerBinding, UserNotificationBinding]],
    ) -> dict[int, list[tuple[UserTriggerBinding, UserNotificationBinding]]]:
        """
        Группирует триггеры и уведомления по data_source_id.

        Args:
            rows: результат JOIN-запроса из БД.

        Returns:
            Словарь: ключ — data_source_id, значение — список пар (триггер, уведомление).
        """
        trigger_map = defaultdict(list)
        for trigger, notification in rows:
            trigger_map[trigger.data_source_id].append((trigger, notification))
        return trigger_map

    async def _run_for_one_source(
        self,
        trigger_items: list[tuple[UserTriggerBinding, UserNotificationBinding]],
        payload: dict,
    ):
        """
        Обрабатывает триггеры и уведомления для одного источника данных.

        Args:
            trigger_items: список триггеров и их уведомлений.
            payload: входные данные, полученные от источника.
        """
        grouped_triggers = self._group_notifications_by_trigger(trigger_items)

        for trigger, notifications in grouped_triggers.items():
            trigger_func = TRIGGER_REGISTRY.get(trigger.trigger_type)
            if not trigger_func:
                continue
            try:
                if trigger_func(payload, trigger.trigger_params):
                    await self._notify(notifications, payload)
            except Exception as e:
                print(f"[!] Trigger error: {e}")

    @staticmethod
    def _group_notifications_by_trigger(
        trigger_items: list[tuple[UserTriggerBinding, UserNotificationBinding]],
    ) -> dict[UserTriggerBinding, list[UserNotificationBinding]]:
        """
        Группирует уведомления по триггерам.

        Args:
            trigger_items: список пар (триггер, уведомление).

        Returns:
            dict: {триггер: [уведомление, ...]}
        """
        grouped_triggers = defaultdict(list)
        for trigger, notif in trigger_items:
            grouped_triggers[trigger].append(notif)
        return grouped_triggers

    @staticmethod
    async def _notify(notifications: list[UserNotificationBinding], payload: dict):
        """
        Кладём задачи в соответствующие очереди; воркеры уже сами дернут NOTIFY_REGISTRY.
        """
        TASK_BY_TYPE = {
                "email": notify_email,
                "tg":    notify_tg,
                "sms":   notify_sms,
            }
        for notif in notifications:
            for notif_type in notif.notification_type:
                task = TASK_BY_TYPE.get(notif_type)
                if not task:
                    # тип не поддержан — пропускаем
                    continue
                try:
                    task.apply_async(
                        args=(payload, notif.notification_config or {}),
                    )
                except Exception as e:
                    print(f"[!] Notification enqueue error ({notif_type}): {e}")