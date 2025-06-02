from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
from app.users.models import User


class UserCreate(BaseModel):
    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Username cannot be empty")
        return value

    email: EmailStr
    password: str

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Password cannot be empty")
        return value

    age: Optional[int] = None


class UserRead(BaseModel):
    id: str
    username: str
    email: EmailStr
    is_active: bool
    age: Optional[int] = None

    @field_validator("id", mode="before")
    @classmethod
    def convert_object_id(cls, value):
        return str(value)

    model_config = {"from_attributes": True}


class UserRef(BaseModel):
    id: str
    username: str

    @field_validator("id", mode="before")
    def convert_id(cls, value):
        return str(value)
    
    # @classmethod
    # def from_user(cls, user: User) -> 'UserRef':
    #     return cls(id=str(user.id), username=user.username)

class UserTask(BaseModel):
    id: str
    username: str

    # @field_validator("id", mode="before")
    # def convert_id(cls, value):
    #     return str(value)
    
    @classmethod
    def from_user(cls, user: User) -> 'UserTask':
        return cls(id=str(user.id), username=user.username)
