from datetime import datetime as dt

from sqlalchemy_utils.types import ChoiceType

from .. import db
from ..helper import PkModel
# from project.modules.users.models import User
from ..users.models import User


user_book = db.Table('user_book',
                     db.Column('book_id', db.Integer, db.ForeignKey('book.id')),
                     db.Column('user_id', db.String(30), db.ForeignKey(User.id)),
                     db.Column('date_borrowed', db.DateTime, nullable=False, default=dt.now()),
                     db.Column('return_date', db.DateTime, nullable=False)
                     )


class Books(PkModel):
    """Model for the books table"""

    CATEGORY = [('maths', 'MATHS'), ('english', 'ENGLISH')]

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False, info={'label': 'Title'})
    classification_no = db.Column(db.String(10), nullable=False, info={'label': 'Classification No.'})
    author = db.Column(db.String(300), nullable=False, info={'label': 'Author'})
    publication = db.Column(db.String(300), nullable=False, info={'label': 'Publication'})
    category = db.Column(ChoiceType(choices=CATEGORY), nullable=False, info={'label': 'Category'})
    comments = db.Column(db.Text, nullable=False, info={'label': 'Comments'})
    date_recorded = db.Column(db.DateTime, nullable=False, default=dt.now())
    # Overall qty = current_qty + spoilt
    qty_added = db.Column(db.Integer, nullable=False)  # Number newly added
    qty_spoilt = db.Column(db.Integer, nullable=False)  # Number spoilt
    current_qty = db.Column(db.Integer, nullable=False)  # The current number in-stock (Current + Added)

    user_id = db.Column(db.String(30), db.ForeignKey(User.id))
    batch = db.relationship('Book', backref='book_batch', lazy=True)

    def __repr__(self):
        return f"<Books-id: {self.id}, Title: {self.title}>"


class Book(PkModel):
    """Model for book table"""
    BOOK_STATUS = [('in-stock', 'in-stock'), ('out-stock', 'out-stock')]

    __tablename__ = "book"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    catalogue_no = db.Column(db.String(50), info={'label': 'Catalogue No.'})
    access_no = db.Column(db.Integer, unique=True, nullable=False, info={'label': 'Access No.'})
    status = db.Column(ChoiceType(BOOK_STATUS), nullable=False)
    is_borrowed = db.Column(db.Boolean, nullable=False, default=False)

    books_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    readers = db.relationship('User', secondary=user_book, backref=db.backref('borrowed_books', lazy=True))

    def __repr__(self):
        return f"<Book-id: {self.id}, Access No.: {self.access_no}>"
