from flask import Blueprint, render_template, flash, redirect, url_for, request
from pathlib import Path
from sqlalchemy.exc import IntegrityError

from .models import Books, Book
from .forms import AddBooksForm
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


# View to add books
@books_bp.route("/add/books", methods=['POST'])
def add_books():
    form = AddBooksForm()
    download_link = request.form.get('download_link')
    catalog = request.form.get('catalogue_no')

    if form.validate():
        print(form.validate_on_submit(), form.data)
        books = Books()
        form.title.data = str(form.title.data).lower()
        form.classification_no.data = str(form.classification_no.data).lower()
        form.author.data = str(form.author.data).lower()
        form.publication.data = str(form.publication.data).lower()
        form.populate_obj(books)

        book_exist = Books.query.filter(Books.classification_no == books.classification_no).first()
        book_instances = []     # list of books_batch
        if book_exist is not None:
            pass
        else:
            books.qty_spoilt, books.current_qty, books.comments = (0, int(form.qty_added.data), download_link)
            # check the last book access number inside a loop == the qty added
            last_book = Book.query.order_by(Book.id.desc()).first()
            last_book_access_no = last_book.access_no if last_book is not None else 0

            for i in range(1, int(form.qty_added.data) + 1):
                # create list of books_batch
                book = Book()
                book.catalogue_no = catalog
                book.access_no = last_book_access_no + i
                book.status = 'available'
                book_instances.append(book)

        try:
            books.batch.extend(book_instances)
            books.insert_many(book_instances)
            flash("Books detail added successfully.", "success")
        except IntegrityError:
            db.session.rollback()
            flash("Books detail not added.", "danger")

    return redirect(url_for(".book_index"))
