from odmantic import Model, Reference, Field, ObjectId
from typing import Optional
from app.users.models import User
from app.users.schemas import UserTask
from pydantic import model_serializer
# from datetime import datetime

class Task(Model):
    id: ObjectId = Field(primary_field=True, default_factory=ObjectId)
    shortname: str
    description: Optional[str] = None
    created_by: User = Reference()
    completed: bool = False
    perms_read: list
    perms_edit: list

    @model_serializer
    def serialize(self) -> dict:
        return {
            "id": str(self.id),
            "shortname": self.shortname,
            "description": self.description,
            "completed": self.completed,
            "created_by": UserTask.from_user(self.created_by),
            "perms_read": self.perms_read,
            "perms_edit": self.perms_edit
            
            #(
            #     {
            #         "id": str(self.created_by.id),
            #         "username": getattr(self.created_by, "username", None),
            #     }
            #     if isinstance(self.created_by, User)
            #     else None
            #)
        }