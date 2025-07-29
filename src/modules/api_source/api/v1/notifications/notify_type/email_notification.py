import os
from email.message import EmailMessage
from dotenv import load_dotenv
import aiosmtplib

from src.modules.api_source.api.v1.notifications.base_type_notify_class import BaseTypeNotificationClass

load_dotenv()


class EmailNotification(BaseTypeNotificationClass):
    """
    Сервис отправки email по SMTP.
    Шаблон письма встроен. Конфигурация (кому и с какими данными) приходит из БД.
    """

    def __init__(self):
        self.smtp_host = os.getenv("SMTP_HOST")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_user = os.getenv("SMTP_USERNAME")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.smtp_user)

    async def send(self, payload: dict, config: dict):
        """
        Args:
            payload: данные от триггера (игнорируются здесь).
            config: конфиг из БД, пример:
                {
                    "email": "user@example.com"
                }
        """
        recipient = config.get("email")
        if not recipient:
            print("[!] Email is not specified in config")
            return

        # Шаблон письма внутри
        subject = "Оповещение от trigger flow"
        body = f"{payload}, {config}"

        message = EmailMessage()
        message["From"] = self.from_email
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        try:
            await aiosmtplib.send(
                message,
                hostname=self.smtp_host,
                port=self.smtp_port,
                username=self.smtp_user,
                password=self.smtp_pass,
                start_tls=True
            )
            print(f"[+] Email was send: {recipient}")
        except Exception as e:
            print(f"[!] Error sending email: {e}")

    def describe(self) -> dict:
        return {
            "description": "Отправляет email.",
            "notification_config": {
                "email": "Email получателя",
            }
        }
