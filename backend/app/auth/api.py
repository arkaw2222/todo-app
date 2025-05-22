from fastapi import APIRouter, Depends, Body
from odmantic import AIOEngine
from app.auth.schemas import SignIn, Code
from app.core.db import get_engine
from app.auth import service
from app.users.models import User
from app.users.schemas import UserCreate
from app.auth.service import get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signin")
async def sign_in(credentials: SignIn, engine: AIOEngine = Depends(get_engine)) -> str:
    return await service.signin(engine, credentials)


@router.post("/signup")
async def sign_up(
    userCreate: UserCreate, engine: AIOEngine = Depends(get_engine)
) -> str:
    return await service.signup(engine, userCreate)


@router.post("/verify")
async def verify_account(
    current_user: User = Depends(get_current_user),
    code: Code = Body(...),
    engine: AIOEngine = Depends(get_engine),
) -> dict:
    return await service.verifyaccount(current_user, code, engine)
