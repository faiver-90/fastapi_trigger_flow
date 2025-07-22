from pydantic import BaseModel
from datetime import datetime


class UserTriggerBindingBase(BaseModel):
    user_id: int
    data_source_id: int
    trigger_id: int
    template_id: int
    is_active: bool | None = True


class UserTriggerBindingCreate(UserTriggerBindingBase):
    pass


class UserTriggerBindingUpdate(BaseModel):
    user_id: int | None
    data_source_id: int | None
    trigger_id: int | None
    template_id: int | None
    is_active: bool | None


class UserTriggerBindingOut(UserTriggerBindingBase):
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
