from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class NotificationTemplate(Base):
    __tablename__ = "notification_templates"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    channel: Mapped[str] = mapped_column(String(50), nullable=False)  # email, telegram, sms и т.д.
