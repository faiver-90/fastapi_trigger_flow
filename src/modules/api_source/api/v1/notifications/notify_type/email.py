from src.modules.api_source.api.v1.notifications.notify_type.base_notify_class import NotificationBaseClass


class EmailNotification(NotificationBaseClass):
    async def send(self, payload, config):
        print(f'Notify email with payload {payload}, config {config}')
