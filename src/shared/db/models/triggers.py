from sqlalchemy import String, Text
from sqlalchemy.orm import mapped_column, Mapped

from src.shared.db.base import Base


class Trigger(Base):
    __tablename__ = "triggers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    condition: Mapped[str] = mapped_column(Text, nullable=False)  # можно DSL, JSON или просто SQL/функция
    description: Mapped[str] = mapped_column(String(512), nullable=True)
