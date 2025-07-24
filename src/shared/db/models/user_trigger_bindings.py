from sqlalchemy import Integer, String, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class UserTriggerBinding(Base):
    __tablename__ = "user_trigger_bindings"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    trigger_type: Mapped[str] = mapped_column(String, nullable=False)
    trigger_params: Mapped[dict] = mapped_column(JSON, nullable=True)
    data_source_id: Mapped[int] = mapped_column(Integer, nullable=False)
