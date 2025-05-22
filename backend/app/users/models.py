from odmantic import Model, ObjectId, Field
from typing import Optional
from datetime import datetime

class User(Model):
    id: ObjectId = Field(primary_field=True, default_factory=ObjectId)
    username: str = Field(unique = True)
    email: str = Field(unique = True)
    age: Optional[int] = None
    is_verified: bool = False
    verification_code: Optional[str] = None
    verification_code_expires: Optional[datetime] = None
    is_active: bool = True
    password: str