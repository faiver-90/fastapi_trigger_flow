from src.modules.api_source.api.v1.notifications.notification_repo import (
    NotificationRepo,
)
from src.shared.services.base_crud_service import BaseCRUDService


class CRUDNotificationService(BaseCRUDService[NotificationRepo]):
    pass
