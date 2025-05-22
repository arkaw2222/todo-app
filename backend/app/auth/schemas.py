from pydantic import BaseModel
from datetime import datetime


class SignIn(BaseModel):
    username: str
    password: str


class JWTPayload(BaseModel):
    sub: str
    exp: datetime


class Code(BaseModel):
    code: int
