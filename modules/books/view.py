from flask import Blueprint, render_template, flash, redirect, url_for, request
from pathlib import Path

from sqlalchemy import or_
from sqlalchemy.exc import IntegrityError

from .models import Books
from .forms import AddBooksForm, SearchBooksForm
# from project.modules.books.models import Books, Book
from .. import db

static_path = Path('.').parent.absolute() / 'modules/static'
books_bp = Blueprint("books", __name__, url_prefix="/books", static_folder=static_path)


# TODO: Remove the book table since it is unnecessary. Instead search for a book using
#  the classification number or the title or author or category
#  and their added as borrowed_users to that book.
#  We then create the user_book table using that the book and user entities.


# View to show book inventory page
@books_bp.route("/add")
def book_index():
    context = {}
    user_log = True
    admin = True  # remove this when user login is implemented
    books_form = AddBooksForm()
    context.update(admin=admin, books_form=books_form, user_log=user_log)
    return render_template("books/add.html", **context)


# View to show page for searching books
@books_bp.route("/list", methods=['GET', 'POST'])
def list_books():
    context = {}
    user_log = True
    admin = True  # remove this when user login is implemented
    search_form = SearchBooksForm()

    if request.method == 'POST':
        search_keyword = str(search_form.search_term.data).lower()
        get_accounts = Books.query.filter(or_(Books.title.regexp_match(search_keyword),
                                              Books.author.regexp_match(search_keyword),
                                              Books.classification_no.regexp_match(search_keyword),
                                              Books.category.regexp_match(search_keyword)
                                              )).all()
        context.update(book_records=get_accounts)
        return render_template("books/records_output.html", **context)

    context.update(admin=admin, search_form=search_form, user_log=user_log)
    return render_template("books/view.html", **context)


# View to add books
@books_bp.route("/add/books", methods=['POST'])
def add_books():
    form = AddBooksForm()

    if form.validate():
        print(form.validate_on_submit(), form.data)
        books = Books()
        form.title.data = str(form.title.data).lower()
        form.classification_no.data = str(form.classification_no.data).lower()
        form.author.data = str(form.author.data).lower()
        form.publication.data = str(form.publication.data).lower()
        form.populate_obj(books)

        book_exist = Books.query.filter(Books.classification_no == books.classification_no).first()
        if book_exist is not None:
            pass
        else:
            last_book = Books.query.order_by(Books.id.desc()).first()
            access_no = last_book.access_no + int(form.qty_added.data)
            books.qty_spoilt, books.current_qty, books.access_no = (0, int(form.qty_added.data), access_no)

        try:
            books.update()
            flash("Books detail added successfully.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Books detail not added.", "danger")

    return redirect(url_for(".book_index"))
