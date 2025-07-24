from pydantic import BaseModel
from typing import Optional


class DataSourceBase(BaseModel):
    user_id: int
    name: str
    is_active: Optional[bool] = True


class DataSourceCreate(DataSourceBase):
    source_key: str


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    is_active: Optional[bool] = None


class DataSourceOut(DataSourceBase):
    id: int

    model_config = {
        "from_attributes": True
    }
