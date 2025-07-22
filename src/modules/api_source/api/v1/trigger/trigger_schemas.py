from pydantic import BaseModel, Field


class TriggerBase(BaseModel):
    name: str = Field(..., max_length=255)
    condition: dict
    user_id: int


class TriggerCreate(TriggerBase):
    pass


class TriggerUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    condition: dict
    user_id: int


class TriggerOut(TriggerBase):
    id: int

    model_config = {
        "from_attributes": True
    }
