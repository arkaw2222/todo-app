from starlette_admin.contrib.odmantic import Admin, ModelView
from app.core.db import get_engine as engine
from app.users.models import User
from app.tasks.models import Task
from app.users.admin import UserView


# Create admin
admin = Admin(engine(), title="Админка")
admin.add_view(UserView(User))
admin.add_view(ModelView(Task))
