from datetime import datetime

from sqlalchemy import DateTime, Boolean, Integer
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class UserTriggerBinding(Base):
    __tablename__ = "user_trigger_bindings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data_source_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    template_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
