from app.users.models import User
from odmantic import AIOEngine
from app.tasks.models import Task
from .schemas import TaskCreate, TaskEdit, TaskRead, TaskPerms
import logging
from fastapi import HTTPException
from odmantic import ObjectId
from typing import cast

logger = logging.getLogger(__name__)


async def create_task(
    engine: AIOEngine, taskCreate: TaskCreate, current_user: User
) -> Task:
    if not current_user.is_verified:
        raise HTTPException(403, "Account not verified")
    try:
        task = Task(
            shortname=taskCreate.shortname,
            description=taskCreate.description,
            created_by=current_user,
            perms_read=[],
            perms_edit=[]
        )
        await engine.save(task)
        return task
    except Exception as e:
        logger.exception("Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def get_tasks_by_status(engine: AIOEngine, completed: bool) -> list[Task]:
    return await engine.find(Task, Task.completed == completed)


async def get_task_by_id(engine: AIOEngine, task_id: ObjectId) -> TaskRead:
    task = await engine.find_one(Task, Task.id == task_id)
    if not task:
        raise HTTPException(404, "Task not found")
    return TaskRead(**task.serialize())


async def get_all_tasks(engine: AIOEngine) -> list[Task]:
    return await engine.find(Task)


async def edit_task(
    engine: AIOEngine, task_id: str, task_data: TaskEdit, current_user: User
) -> Task:
    if not current_user.is_verified:
        raise HTTPException(403, "Account not verified")
    try:
        task = await engine.find_one(Task, Task.id == ObjectId(task_id))
        if not task:
            raise HTTPException(404, "Task not found")
        if task.created_by.id != current_user.id:
            raise HTTPException(403, "Permission denied")
        edit_data = task_data.model_dump(exclude_unset=True)
        for key, value in edit_data.items():
            setattr(task, key, value)
        await engine.save(task)
        return cast(Task, await get_task_by_id(engine, task.id))
    except Exception as e:
        logger.exception("Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal Server Error")


async def delete_task(engine: AIOEngine, task_id: str, current_user: User) -> None:
    if not current_user.is_verified:
        raise HTTPException(403, "Account not verified")
    try:
        task = await engine.find_one(Task, Task.id == ObjectId(task_id))
        if not task:
            raise HTTPException(404, "Task not found")
        if task.created_by.id != current_user.id:
            raise HTTPException(403, "Permission denied")
        await engine.delete(task)
    except Exception as e:
        logger.exception("Internal Server Error")
        raise HTTPException(status_code=500, detail="Internal Server Error")

async def change_read(engine: AIOEngine, current_user: User, task_id: str, users: list[str]) -> None:
    try:
        task = await engine.find_one(Task, Task.id == task_id)

        if not task:
            raise HTTPException(404, 'Task not found')
        if task.created_by != current_user:
            raise HTTPException(403, 'Permission denied')
        # if users.issubset(task.perm_read):
        #     raise HTTPException(422, 'Already provided')
        
        task.perms_read = users

    except Exception as e:
        logger.exception('Internal Server Error')
        raise HTTPException(500, 'Internal Server Error')

async def change_edit(engine: AIOEngine, current_user: User, task_id: str, users: list[str]) -> None:
    try:
        task = await engine.find_one(Task, Task.id == task_id)

        if not task:
            raise HTTPException(404, 'Task not found')
        if task.created_by != current_user:
            raise HTTPException(403, 'Permission denied')
        # if users.issubset(task.perm_edit):
        #     raise HTTPException(422, 'Already provided')
        
        task.perms_edit = users

    except Exception as e:
        logger.exception('Internal Server Error')
        raise HTTPException(500, 'Internal Server Error')

async def get_task_permissions(engine: AIOEngine, task_id: str, current_user = User) -> TaskPerms:
    try:
        task = await engine.find_one(Task, Task.id == task_id)
        if not task:
            raise HTTPException(404, 'Task not found')
        if task.created_by != current_user:
            raise HTTPException(403, 'Permission denied')
        return TaskPerms(**task.dict())

    except Exception as e:
        logger.exception('Internal Server Error')
        raise HTTPException(500, 'Internal Server Error')


    




