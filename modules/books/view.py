from flask import Blueprint

from .models import Books, Book
# from project.modules.books.models import Books, Book


books_bp = Blueprint("books", __name__, url_prefix="/books")
