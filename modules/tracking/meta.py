from datetime import datetime as dt

from project.modules import db
from ..books.models import Book
from ..users.models import User


user_book = db.Table('user_book',
                     db.Column('book_id', db.Integer, db.ForeignKey(Book.id)),
                     db.Column('user_id', db.String(30), db.ForeignKey(User.id)),
                     db.Column('date_borrowed', db.DateTime, nullable=False, default=dt.now()),
                     db.Column('return_date', db.DateTime, nullable=False)
                     )
