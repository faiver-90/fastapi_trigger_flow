from pydantic import BaseModel
from typing import Optional


class DataSourceBase(BaseModel):
    user_id: int
    is_active: Optional[bool] = True


class DataSourceCreate(DataSourceBase):
    source_key: str
    data_source_id: int


class DataSourceUpdate(BaseModel):
    is_active: Optional[bool] = None


class DataSourceOut(DataSourceBase):
    id: int

    model_config = {
        "from_attributes": True
    }
