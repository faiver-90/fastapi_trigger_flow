from sqlalchemy import String, Integer, Boolean, JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.shared.db.base import Base


class DataSource(Base):
    __tablename__ = "data_sources"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, server_default="true")
    source_key: Mapped[str] = mapped_column(String(255), nullable=False, server_default='default_key')
    data_source_id: Mapped[int] = mapped_column(Integer, nullable=False)
