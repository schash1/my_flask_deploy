from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..models.database import db
from ..models.user import User
from ..permissions.user import UserListPermission, \
    UserPatchPermission
from ..schemas.user import UserSchema


class UserList(ResourceList):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        'permission_get': [UserListPermission],
    }


class UserDetail(ResourceDetail):
    schema = UserSchema
    data_layer = {
        "session": db.session,
        "model": User,
        'permission_get': [UserListPermission],
        'permission_patch': [UserPatchPermission],
    }
