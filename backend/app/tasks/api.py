from fastapi import APIRouter, Depends, Query
from odmantic import AIOEngine
from app.auth.service import get_current_user as current_user
from app.core.db import get_engine
from app.tasks import service, schemas, models
from typing import Optional
from app.users.models import User
from app.tasks.models import Task


router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post("/", response_model=schemas.TaskRead)
async def create_task(
    data: schemas.TaskCreate,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user),
) -> dict:
    task = await service.create_task(engine, data, user)
    task = task.serialize()
    return task


@router.get("/")
async def list_tasks_by_status(
    completed: Optional[bool] = Query(None), engine: AIOEngine = Depends(get_engine)
) -> list[models.Task]:
    if completed == None:
        return await service.get_all_tasks(engine)
    # elif completed == False:
    return await service.get_tasks_by_status(engine, completed)
    # return service.get_all_tasks(engine) #возвращать выполненные


@router.get("/get_my_tasks")
async def get_my_tasks(
    user: User = Depends(current_user),
    engine: AIOEngine = Depends(get_engine)
) -> list[Task]:
    return await service.get_my_tasks(engine, user)


@router.patch("/{task_id}/edit", response_model=schemas.TaskRead)
async def edit_task(
    task_id: str,
    data: schemas.TaskEdit,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user),
) -> Task:
    return await service.edit_task(engine, task_id, data, user)


@router.delete("/{task_id}", status_code=204)
async def delete_task(
    task_id: str,
    engine: AIOEngine = Depends(get_engine),
    user: User = Depends(current_user),
):
    await service.delete_task(engine, task_id, user)


@router.patch('/{task_id}/change_read')
async def change_read_permission(
    task_id: str,
    users: list[str],
    user: User = Depends(current_user),
    engine: AIOEngine = Depends(get_engine)
) -> None:
    """
    Note: list `users` will **OVERWRITE** current permissions

    Firstly get current permissions by router `get_task_permissions`

    Secondary modify list `users`

    Thirdly fill request body
    """
    return await service.change_read(engine, user, task_id, users)

@router.patch('/{task_id}/change_edit')
async def change_edit_permission(
    task_id: str,
    users: list[str],
    user: User = Depends(current_user),
    engine: AIOEngine = Depends(get_engine)
) -> None:
    """
    Note: list `users` will **OVERWRITE** current permissions

    Firstly get current permissions by router `get_task_permissions`

    Secondary modify list `users`

    Thirdly fill request body
    """
    return await service.change_edit(engine, user, task_id, users)


@router.get('/{task_id}/get_perms')
async def get_task_permissions(
    task_id: str,
    user: User = Depends(current_user),
    engine: AIOEngine = Depends(get_engine),
):
    return await service.get_task_permissions(engine, task_id, user) #type: ignore
