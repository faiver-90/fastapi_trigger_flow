from src.modules.api_source.api.v1.notifications.base_notify_class import NotificationBaseClass


class EmailNotification(NotificationBaseClass):
    async def send(self, payload, config):
        print(f'Notify email with payload {payload}, config {config}')

    def describe(cls) -> dict:
        return {
            "descriptions": "Отправляет оповещение на почту"
        }
