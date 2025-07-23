from src.modules.api_source.api.v1.notifications.notify_type.base_notify_class import NotificationBaseClass


class ConsoleNotification(NotificationBaseClass):
    async def send(self, payload: dict, config: dict):
        print(f'Notify console with payload {payload}, config {config}')

