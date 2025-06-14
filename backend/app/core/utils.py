from odmantic import Model
from typing import TypeVar
from passlib.context import CryptContext

T = TypeVar("T", bound=Model)


def model_to_clean_dict(model: T) -> T:
    data = model.dict()
    data["id"] = str(model.id)
    return data  # type: ignore


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)
