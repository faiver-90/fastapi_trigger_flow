from typing import Any

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
