from flask import Blueprint, render_template

from ..models.author import Author

authors_app = Blueprint("authors_app", __name__)


@authors_app.route("/", endpoint="list")
def authors_list():
    authors = Author.query.all()
    return render_template("authors/list.html", authors=authors)
