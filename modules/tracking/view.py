from datetime import datetime as dt

from .forms import IssueBookForm, SearchBooksForm
from project.modules.books.models import Books, UserBooksHistory, User

from flask import Blueprint, render_template, request
from sqlalchemy import or_
# from sqlalchemy.exc import IntegrityError

tracking_bp = Blueprint("tracking", __name__, url_prefix="/tracking")


# TODO: Add route for searching books borrowed. Results should filtered to books borrowed in the last 30 days
# TODO: Add route for searching users reading a specific book
# TODO: Add route for searching books borrowed by a user
# TODO: If user_id or name is not provided, then search all books borrowed by users.
#  Show the name & ID of user or book title on top of the results table when displaying results
# TODO: Use the tab navigation panel to show different search fields (search by book name and classification no.,
#  search by user name and sid, or show all results).
#  With the show all results, when the user clicks on the tab, it should send a request for all borrowed books.

# View to return books record after search
@tracking_bp.route("/get_books", methods=['POST'])
def tracking_index():
    context = {}
    search_form = SearchBooksForm()
    issue_form = IssueBookForm()
    search_keyword = str(search_form.search_term.data).lower()
    get_books = Books.query.filter(or_(Books.title.regexp_match(search_keyword),
                                       Books.author.regexp_match(search_keyword),
                                       Books.classification_no.regexp_match(search_keyword),
                                       Books.category.regexp_match(search_keyword)
                                       )).all()
    context.update(book_records=get_books, issue_form=issue_form)
    return render_template("books_history/records_output.html", **context)


# View to assign book(s) to users
@tracking_bp.route("/issue_book", methods=['POST'])
def issue_book():
    issue_form = IssueBookForm()
    book_id = request.form.get('bk_id', type=int)

    if book_id is not None and issue_form.validate():
        user: User = issue_form.borrowed_by.data
        book: Books = Books.get_by_id(book_id)
        user_book_history = UserBooksHistory()
        # Add issued book record to user_book_history table
        user_book_history.book_id = book_id
        user_book_history.user_id = user.id
        user_book_history.return_date = issue_form.return_date.data
        # Add issued book record to user_book table which is a M2M relationship between User and Books models
        book.readers.append(user)
        book.update()
        user_book_history.update()

        msg = f"Book assigned to {user.sid.replace('_', '/')}."

        return f"""
<li class="breadcrumb-item disappear" id="feedback">
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
      <symbol id="check-circle-fill" fill="currentColor" viewBox="0 0 16 16">
        <path d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zm-3.97-3.03a.75.75 0 0 0-1.08.022L7.477 9.417 5.384 7.323a.75.75 0 0 0-1.06 1.06L6.97 11.03a.75.75 0 0 0 1.079-.02l3.992-4.99a.75.75 0 0 0-.01-1.05z"/>
      </symbol>
    </svg>
        
    <span class="alert alert-success" role="alert">
        <svg width="30" height="20" role="img" aria-label="Success:"><use xlink:href="#check-circle-fill"/></svg>
        <span>{msg}</span>
    </span>
</li>
"""

    msg = "Book not assigned to user. Try searching again."

    return f"""
<li class="breadcrumb-item disappear" id="feedback">
    <svg xmlns="http://www.w3.org/2000/svg" style="display: none;">
        <symbol id="exclamation-triangle-fill" fill="currentColor" viewBox="0 0 16 16">
            <path d="M8.982 1.566a1.13 1.13 0 0 0-1.96 0L.165 13.233c-.457.778.091 1.767.98 1.767h13.713c.889 0 1.438-.99.98-1.767L8.982 1.566zM8 5c.535 0 .954.462.9.995l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 5.995A.905.905 0 0 1 8 5zm.002 6a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
        </symbol>
    </svg>
    <span class="alert alert-warning" role="alert">
        <svg width="30" height="20" role="img" aria-label="Warning:"><use xlink:href="#exclamation-triangle-fill"/></svg>
        <span>{msg}</span>
    </span>
</li>
"""


# View to return books(s) by users

# View to search user_book history by user_sid
# @tracking_bp.route("/search_by_user_id")
# def search_by_user_id():
#     context = {}
#     search_form = SearchByUserIdForm()
#     get_user_id = User.query.filter(
#         User.sid == str(search_form.keyword.data).replace('/', '_')
#     ).first()
#     get_records = UserBooksHistory.query.filter(UserBooksHistory.user_id == get_user_id.id).all()
#     context.update(book_records=get_books, issue_form=issue_form)
#     return render_template("books_history/records_output.html", **context)

# View to search user_book history by issue or return date

# View to search user_book history by book title

