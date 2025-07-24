from sqlalchemy import Integer, String, JSON, ARRAY, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class UserCompiledTriggerData(Base):
    __tablename__ = "user_compiled_trigger_data"

    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    user_trigger_id: Mapped[int] = mapped_column(Integer, nullable=False)
    data_source_id: Mapped[int] = mapped_column(Integer, nullable=False)

    data_source_name: Mapped[str] = mapped_column(String(255), nullable=False)
    data_source_is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, server_default="true")
    source_key: Mapped[str] = mapped_column(String(255), nullable=False)

    trigger_type: Mapped[str] = mapped_column(String, nullable=False)
    trigger_params: Mapped[dict] = mapped_column(JSON, nullable=True)

    notification_type: Mapped[list[str]] = mapped_column(ARRAY(String), nullable=False)
    notification_config: Mapped[dict] = mapped_column(JSON, nullable=True)
