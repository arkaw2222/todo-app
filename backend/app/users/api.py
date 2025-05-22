from fastapi import APIRouter, Depends
from odmantic import AIOEngine
from app.core.db import get_engine  
from app.users import service, schemas

router = APIRouter(prefix="/users", tags=["Users"])

# @router.post("/", response_model=schemas.UserRead)
# async def create_user(data: schemas.UserCreate, engine: AIOEngine = Depends(get_engine)):
#     return await service.create_user(engine, data)

@router.get("/", response_model=list[schemas.UserRead])
async def list_users(engine: AIOEngine = Depends(get_engine)):
    return await service.get_all_users(engine)
