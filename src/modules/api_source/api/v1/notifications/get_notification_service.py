from src.modules.api_source.api.v1.notifications.notification_repo import NotificationRepo
from src.modules.api_source.api.v1.notifications.notification_service import CRUDNotificationService
from src.shared.services.base_get_service import base_get_service

get_notification_service = base_get_service(CRUDNotificationService, NotificationRepo)
