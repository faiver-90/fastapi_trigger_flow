from pydantic import BaseModel
from typing import Optional, Dict


class DataSourceBase(BaseModel):
    user_id: int
    name: str
    credentials: Dict[str, str]
    is_active: Optional[bool] = True


class DataSourceCreate(DataSourceBase):
    pass


class DataSourceUpdate(BaseModel):
    name: Optional[str] = None
    credentials: Optional[Dict[str, str]] = None
    is_active: Optional[bool] = None


class DataSourceOut(DataSourceBase):
    id: int

    model_config = {
        "from_attributes": True
    }
