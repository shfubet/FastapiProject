from pydantic import BaseModel, ConfigDict


class UserDetail(BaseModel):
    model_config = ConfigDict(from_attributes=True)
