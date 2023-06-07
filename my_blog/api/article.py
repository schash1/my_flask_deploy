from combojsonapi.event.resource import EventsResource
from flask_combo_jsonapi import ResourceDetail, ResourceList

from ..models.article import Article
from ..models.database import db
from ..permissions.article import UserPermissionArticle, \
    UserListPermissionArticle
from ..schemas.article import ArticleSchema


class ArticleListEvents(EventsResource):
    def event_get_count(self, **kwargs):
        return {"count": Article.query.count()}


class ArticleList(ResourceList):
    events = ArticleListEvents
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        'permission_get': [UserListPermissionArticle],
    }


class ArticleDetail(ResourceDetail):
    schema = ArticleSchema
    data_layer = {
        "session": db.session,
        "model": Article,
        'permission_get': [UserListPermissionArticle],
        'permission_patch': [UserPermissionArticle],
    }
