from typing import Any, List, Dict

from pydantic import BaseModel, Field


class TriggerBase(BaseModel):
    user_id: int
    trigger_type: str
    trigger_params: dict[str, Any] | None = Field(default_factory=dict)
    data_source_id: int


class TriggerCreate(TriggerBase):
    pass


class TriggerUpdate(BaseModel):
    trigger_params: dict[str, Any] | None = None
    data_source_id: int | None = None


class TriggerOut(TriggerBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class NotificationCreate(BaseModel):
    notification_type: List[str]
    notification_config: Dict[str, Any] = Field(default_factory=dict)


class TriggerWithNotificationsCreate(BaseModel):
    trigger_type: str
    trigger_params: Dict[str, Any] = Field(default_factory=dict)
    notifications: List[NotificationCreate]


class BulkTriggerCreate(BaseModel):
    data_source_id: int
    user_id: int
    triggers: List[TriggerWithNotificationsCreate]
