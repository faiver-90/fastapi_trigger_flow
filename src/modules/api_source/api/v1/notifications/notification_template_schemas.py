from pydantic import BaseModel, Field


class NotificationTemplateBase(BaseModel):
    title: str = Field(..., max_length=255)
    body: str
    channel: str = Field(..., max_length=50)


class NotificationTemplateCreate(NotificationTemplateBase):
    pass


class NotificationTemplateUpdate(BaseModel):
    title: str | None = Field(None, max_length=255)
    body: str | None
    channel: str | None = Field(None, max_length=50)


class NotificationTemplateOut(NotificationTemplateBase):
    id: int

    model_config = {
        "from_attributes": True
    }
