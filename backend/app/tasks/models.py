from odmantic import Model, Reference, Field, ObjectId
from typing import Optional
from app.users.models import User
from app.users.schemas import UserRef
from pydantic import model_serializer
# from datetime import datetime

class Task(Model):
    id: ObjectId = Field(primary_field=True, default_factory=ObjectId)
    shortname: str
    description: Optional[str] = None
    created_by: User = Reference()
    completed: bool = False

    @model_serializer
    def serialize(self) -> dict:
        return {
            "id": str(self.id),
            "shortname": self.shortname,
            "description": self.description,
            "completed": self.completed,
             "created_by": UserRef.from_user(self.created_by)#(
            #     {
            #         "id": str(self.created_by.id),
            #         "username": getattr(self.created_by, "username", None),
            #     }
            #     if isinstance(self.created_by, User)
            #     else None
            #)
        }