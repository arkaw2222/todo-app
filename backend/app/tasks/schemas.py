from pydantic import BaseModel, field_validator, ConfigDict
from typing import Optional
from app.users.schemas import UserRef


class TaskCreate(BaseModel):
    shortname: str
    description: Optional[str] = None

    @field_validator("shortname")
    def validate_shortname(cls, v):
        if len(v) < 6:
            raise ValueError("Название задачи слишком короткое")
        return v


class TaskRead(BaseModel):
    id: str
    shortname: str
    description: Optional[str] = None
    created_by: UserRef
    completed: bool

    @field_validator("id", mode="before")
    def convert_id(cls, value):
        return str(value)

    model_config = ConfigDict(from_attributes=True)


class TaskEdit(BaseModel):
    shortname: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "shortname": "Название",
                "description": "Описание",
                "completed": True,
            }
        }
    )

class TaskPerms(BaseModel):
    id: str
    shortname: str
    perms_read: list
    perms_edit: list
