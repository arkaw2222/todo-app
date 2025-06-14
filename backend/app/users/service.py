from odmantic import AIOEngine
from app.users.models import User
from .schemas import UserCreate
from fastapi import HTTPException
import logging
from datetime import datetime, timedelta
from random import randint
from app.core.utils import hash_password


logger = logging.getLogger(__name__)


async def create_user(engine: AIOEngine, userCreate: UserCreate) -> User:
    
    verification_code = f"{randint(0, 999999):06d}"

    try:
        user = User(
            username = userCreate.username,
            email = userCreate.email,
            password = await hash_password(userCreate.password),
            age = userCreate.age,
            is_active = True,
            verification_code = verification_code,
            verification_code_expires = datetime.now() + timedelta(minutes = 60)

        )
        await engine.save(user)
        return user
    except Exception as e:
        logger.exception("Ошибка при создании пользователя")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_user_by_email(engine: AIOEngine, email: str) -> User | None:
    return await engine.find_one(User, User.email == email)


async def get_all_users(engine: AIOEngine) -> list[User]:
    return await engine.find(User)


async def get_user_by_username(engine: AIOEngine, username: str) -> User | None:
    return await engine.find_one(User, User.username == username)

async def get_user_by_partusername(engine: AIOEngine, data: str, page: int) -> list:
    return await engine.find(model = User, queries = User.username.match(f".*{data}.*"), limit = 20, skip = page*20) # type: ignore