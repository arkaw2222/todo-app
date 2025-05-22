from starlette_admin.contrib.odmantic import ModelView
from app.auth.service import hash_password

class UserView(ModelView):
    fields = [
        'id',
        'username',
        'email',
        'age',
        'is_active',
        'password'
    ]

    # async def before_create(self, request, data, obj):
    #     obj.password = await hash_password(obj.password)

    async def before_edit(self, request, data, obj):
        if not obj.password[:4:] == '$2b$':
            obj.password = await hash_password(obj.password)