from sqlalchemy import Integer, String, JSON, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class UserNotificationBinding(Base):
    __tablename__ = "user_notification_bindings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    notification_type: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    notification_config: Mapped[dict] = mapped_column(JSON, nullable=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
