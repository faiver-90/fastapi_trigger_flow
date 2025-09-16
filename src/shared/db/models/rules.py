from sqlalchemy import Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class Rules(Base):
    __tablename__ = "rules"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=True)
    source_id: Mapped[int] = mapped_column(Integer, nullable=True)
    trigger_id: Mapped[int] = mapped_column(Integer, nullable=True)
    user_notification_id: Mapped[int] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=True)
