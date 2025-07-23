from src.modules.api_source.api.v1.notifications.notify_type.console import ConsoleNotification
from src.modules.api_source.api.v1.notifications.notify_type.email import EmailNotification

NOTIFY_REGISTRY = {
    "email": EmailNotification(),
    "console": ConsoleNotification()
}
