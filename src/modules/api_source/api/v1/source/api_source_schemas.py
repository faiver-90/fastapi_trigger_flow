from pydantic import BaseModel


class DataSourceBase(BaseModel):
    user_id: int
    is_active: bool | None = True


class DataSourceCreate(DataSourceBase):
    source_key: str
    data_source_id: int


class DataSourceUpdate(BaseModel):
    is_active: bool | None = None


class DataSourceOut(DataSourceBase):
    id: int

    model_config = {"from_attributes": True}
