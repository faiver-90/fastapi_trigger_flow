from src.modules.api_source.api.v1.notifications.base_type_notify_class import BaseTypeNotificationClass


class EmailNotification(BaseTypeNotificationClass):
    async def send(self, payload, config):
        print(f'Notify email with payload {payload}, config {config}')

    def describe(cls) -> dict:
        return {
            "descriptions": "Отправляет оповещение на почту"
        }
