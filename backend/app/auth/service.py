from os import getenv
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from odmantic import AIOEngine
from app.core.db import get_engine
from app.users.models import User
from app.users.schemas import UserCreate
from app.users.service import create_user, get_user_by_username
from .schemas import JWTPayload, SignIn
from jose import ExpiredSignatureError, JWTError, jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.auth.schemas import Code
from app.core.email import send_verification_code

SECRET_KEY = str(getenv("SECRET_KEY"))
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def hash_password(password: str) -> str:
    return pwd_context.hash(password)


async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def jwt_generate(username: str) -> str:
    expire = datetime.now() + timedelta(minutes=60)
    payload = {"sub": username, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


async def jwt_decode(token: str) -> JWTPayload:
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms="HS256", options={"verify_exp": True}
        )
        return JWTPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except JWTError:
        raise HTTPException(401, "Invalid token")


async def signin(engine: AIOEngine, credentials: SignIn) -> str:
    """
    This function returns JWT-Token
    """
    user = await get_user_by_username(engine, credentials.username)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    # if not user.is_verified:
    #     raise HTTPException(403, 'Account not verified')
    if not await verify_password(credentials.password, user.password):
        raise HTTPException(401, "Wrong password")
    return await jwt_generate(user.username)


async def signup(engine: AIOEngine, userCreate: UserCreate) -> str:
    """
    Returns JWT-Token
    """
    u = userCreate.model_copy(
        update={
            "password": await hash_password(userCreate.password),
        }
    )
    user = await create_user(engine, u)


    if not user.verification_code:
        raise HTTPException(500, "Ошибка генерации кода")
    
    await send_verification_code(user.email, user.verification_code)

    return await signin(
        engine, SignIn(username=userCreate.username, password=userCreate.password)
    )


security = HTTPBearer()  # Это парсит Authorization: Bearer <token>


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    engine: AIOEngine = Depends(get_engine),
) -> User:
    """
    Returns current user from DB
    """
    token = credentials.credentials
    payload = await jwt_decode(token)
    user = await get_user_by_username(engine, payload.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


async def verifyaccount(
    user,
    code: Code,
    engine: AIOEngine = Depends(get_engine),
) -> dict:
    """
    Returns error-code or success-message
    """
    if not user:
        raise HTTPException(404, "Not authorizated")
    
    if user.is_verified:
        raise HTTPException(400, "Account is already verified")
    
    if code.code != user.verification_code:
        raise HTTPException(400, "Invalid code")
    
    if user.verification_code_expires < datetime.now():
        raise HTTPException(400, "Expired code")

    user.is_verified = True
    user.verification_code = None
    user.verification_code_expires = None

    await engine.save(user)
    return {"message": "Account verified successfully"}
