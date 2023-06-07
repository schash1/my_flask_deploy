from typing import Dict

import requests
from flask import Blueprint, render_template, request, current_app, redirect, \
    url_for
from flask_login import login_required, current_user
from flask_wtf import form
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from werkzeug.exceptions import NotFound


from ..forms.article import CreateArticleForm
from ..models.article import Article
from ..models.author import Author
from ..models.tag import Tag
from ..models.database import db

articles_app = Blueprint("articles_app", __name__)
users_app = Blueprint("users_app", __name__)


@articles_app.route("/", endpoint="list")
def articles_list():
    articles = Article.query.all()
    # count_articles: Dict = requests.get('http://flask-deploy-vtwe.onrender.com/api/articles/event_get_count/').json()
    # count_articles: Dict = requests.get('http://127.0.0.1:5000/api/articles/event_get_count/').json()
    return render_template("articles/list.html", articles=articles,
                           # count_articles=count_articles['count'],
                          )


@articles_app.route("/<int:article_id>/", endpoint="details")
def article_details(article_id: int):
    article = Article.query.filter_by(id=article_id).options(
        joinedload(Article.tags)  # подгружаем связанные теги!
        ).one_or_none()
    if article is None:
        raise NotFound
    if request.method == "POST" and form.validate_on_submit():  # при создани истатьи
        if form.tags.data:  # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                article.tags.append(tag)  # добавляем выбранные теги к статье
    return render_template("articles/details.html", article=article)


@articles_app.route("/create/", methods=["GET", "POST"], endpoint="create")
@login_required
def create_article():
    error = None
    form = CreateArticleForm(request.form)
    # добавляем доступные теги в форму
    form.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by("name")]
    if request.method == "POST" and form.validate_on_submit():  # при создании статьи
        _article = Article(title=form.title.data.strip(), body=form.body.data)
        if form.tags.data: # если в форму были переданы теги (были выбраны)
            selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data))
            for tag in selected_tags:
                _article.tags.append(tag) # добавляем выбранные теги к статье
        if current_user.author:
            # use existing author if present
            _author = current_user.author
            _article.author_id = _author.id
        else:
            # otherwise create author record
            author = Author(user_id=current_user.id)
            db.session.add(author)
            db.session.flush()
            _article.author_id = author.id
        db.session.add(_article)
        try:
            db.session.commit()
        except IntegrityError:
            current_app.logger.exception("Could not create a new article!")
            error = "Could not create article!"
        else:
            return redirect(
                url_for("articles_app.details", article_id=_article.id))
    return render_template("articles/create.html", form=form, error=error)
