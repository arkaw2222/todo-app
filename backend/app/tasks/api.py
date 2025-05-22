from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine
from app.auth.service import get_current_user as current_user
from app.core.db import get_engine  
from app.tasks import service, schemas, models
from typing import Optional
from app.users.models import User
from app.tasks.schemas import TaskRead, TaskEdit
from app.tasks.models import Task



router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model = TaskRead)
async def create_task(
    data: schemas.TaskCreate,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user)
) -> dict:
    task = await service.create_task(engine, data, user)
    task = task.serialize()
    return task


@router.get("/")
async def list_tasks_by_status(completed: Optional[bool] = Query(None), engine: AIOEngine = Depends(get_engine)) -> list[models.Task]:
    if completed == None:
        return await service.get_all_tasks(engine)
    # elif completed == False:
    return await service.get_tasks_by_status(engine, completed)
    # return service.get_all_tasks(engine) #возвращать выполненные


@router.patch("/{task_id}", response_model=TaskRead)
async def edit_task(
    task_id: str,
    data: TaskEdit,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user)
) -> Task:
    return await service.edit_task(engine, task_id, data, user)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user)
):
    await service.delete_task(engine, task_id, user)