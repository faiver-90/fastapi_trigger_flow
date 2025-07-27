from typing import Any

from pydantic import BaseModel, Field


class NotificationBase(BaseModel):
    user_trigger_id: int
    notification_type: list[str]
    # notification_config: dict[str, Any] | None = Field(default_factory=dict)


class NotificationCreate(NotificationBase):
    pass


class NotificationUpdate(BaseModel):
    notification_type: list[str] | None = None
    notification_config: dict[str, Any] | None = None


class NotificationOut(NotificationBase):
    id: int

    model_config = {
        "from_attributes": True
    }
