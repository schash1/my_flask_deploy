from combojsonapi.permission.permission_system import (
    PermissionMixin,
    PermissionUser,
    PermissionForGet,
    PermissionForPatch,
)
from flask_combo_jsonapi.exceptions import AccessDenied
from flask_login import current_user

from ..models.article import Article


class UserPermissionArticle(PermissionMixin):
    PATCH_AVAILABLE_FIELDS = [
        'title',
        'body',
        'tags',
    ]

    def patch_permission(self, *args, user_permission: PermissionUser = None,
                         **kwargs) -> PermissionForPatch:
        self.permission_for_patch.allow_columns = (
            self.PATCH_AVAILABLE_FIELDS, 10)
        # if not current_user.is_authenticated :
        # raise AccessDenied('No access')
        return self.permission_for_patch

    def patch_data(self, *args, data: dict = None, obj: Article = None,
                   user_permission: PermissionUser = None, **kwargs) -> dict:
        permission_for_patch = user_permission.permission_for_patch_permission(
            model=Article)
        if not current_user.author.id == obj.author_id:
            if not current_user.admin:
                raise AccessDenied('No access')
        return {
            i_key: i_val
            for i_key, i_val in data.items()
            if i_key in permission_for_patch.columns
        }


class UserListPermissionArticle(PermissionMixin):
    ALL_AVAILABLE_FIELDS = (
        'id',
        'author_id',
        'author',
        'title',
        'body',
        'dt_created',
        'dt_updated',
        'tags',
    )

    def get(self, *args, many=True, user_permission: PermissionUser = None,
            **kwargs) -> PermissionForGet:
        if not current_user.is_authenticated:
            raise AccessDenied('No access')

        self.permission_for_get.allow_columns = (self.ALL_AVAILABLE_FIELDS, 10)

        return self.permission_for_get
