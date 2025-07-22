from pydantic import BaseModel, Field


class TriggerBase(BaseModel):
    name: str = Field(..., max_length=255)
    condition: str
    description: str | None = Field(None, max_length=512)


class TriggerCreate(TriggerBase):
    pass


class TriggerUpdate(BaseModel):
    name: str | None = Field(None, max_length=255)
    condition: str | None
    description: str | None = Field(None, max_length=512)


class TriggerOut(TriggerBase):
    id: int

    model_config = {
        "from_attributes": True
    }
