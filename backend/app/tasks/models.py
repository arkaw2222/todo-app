from odmantic import Model, Reference, Field, ObjectId
from typing import Optional
from app.users.models import User
from app.users.schemas import UserRef
from pydantic import model_serializer

class Task(Model):
    id: ObjectId = Field(primary_field=True, default_factory=ObjectId)
    shortname: str
    description: Optional[str] = None
    created_by: User = Reference()
    completed: bool = False
    perms_read: list[str]
    perms_edit: list[str]

    @model_serializer
    def serialize(self) -> dict:
        return {
            "id": str(self.id),
            "shortname": self.shortname,
            "description": self.description,
            "completed": self.completed,
            "created_by": UserRef(id=str(self.created_by.id), username=self.created_by.username),
            "perms_read": self.perms_read,
            "perms_edit": self.perms_edit
        }