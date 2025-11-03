from app.auth_service.src.modules.notifications.repository.notification_repo import (
    NotificationRepo,
)
from app.auth_service.src.shared.services.base_crud_service import BaseCRUDService


class CRUDNotificationService(BaseCRUDService[NotificationRepo]):
    pass
