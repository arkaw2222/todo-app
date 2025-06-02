from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine
from app.core.db import get_engine
from app.users import service, schemas

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[schemas.UserRead])
async def list_users(engine: AIOEngine = Depends(get_engine)):
    return await service.get_all_users(engine)


@router.post("/create_user", response_model=schemas.UserRead)
async def create_user(
    data: schemas.UserCreate, engine: AIOEngine = Depends(get_engine)
):
    return await service.create_user(engine, data)


@router.get("/get_by_part_username", response_model=list[schemas.UserRef])
async def get_by_part_username(
    page: int = Query(
        default=0,
        title="Page number (gt -1)",
        description="The number of list users page()",
        example=1,
        gt=-1,
    ),
    data: str = Query(
        title="Part of username",
        description="Part of username, which used to find users",
        example='abc'
    ),
    engine: AIOEngine = Depends(get_engine),
):
    return await service.get_user_by_partusername(engine, data, page)
