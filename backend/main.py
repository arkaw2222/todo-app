from dotenv import load_dotenv

load_dotenv()
from fastapi import FastAPI
import os
from app.users.api import router as users_router
from app.tasks.api import router as tasks_router
from app.auth.api import router as auth_router
from app.admin.admin import admin
from fastapi import FastAPI


# Получаем переменные из среды
print(os.getenv("MONGO_URL"))

# FastAPI app
app = FastAPI()

app.include_router(users_router)
app.include_router(tasks_router)    
app.include_router(auth_router)


@app.get("/")
async def root():
    return {"message": "ToDo API работает 💚"}


admin.mount_to(app)
