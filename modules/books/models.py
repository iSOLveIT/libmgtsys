from datetime import datetime as dt

from sqlalchemy.orm import backref
from sqlalchemy_utils.types import ChoiceType

from .. import db
from ..db_helper import PkModel

# from project.modules.users.models import User
from ..users.models import User


user_book = db.Table(
    "user_book",
    db.Column("books_id", db.Integer, db.ForeignKey("books.id")),
    db.Column("user_id", db.Integer, db.ForeignKey(User.id)),
)


class UserBooksHistory(PkModel):
    """Model for recording users history with books"""

    __tablename__ = "user_books_history"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"))
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))
    date_borrowed = db.Column(db.DateTime, nullable=False, default=dt.now())
    return_date = db.Column(db.DateTime, nullable=False)

    user_history = db.relationship(
        "User", backref="history", lazy=True
    )  # Links with the User model
    book_history = db.relationship(
        "Books", backref="history", lazy=True
    )  # Links with the Books model

    def __repr__(self):
        return f"<Issue Date: {self.date_borrowed}, Return Date: {self.return_date}>"


class Books(PkModel):
    """Model for the books table"""

    CATEGORY = [
        ("", ""),
        ("maths", "MATHS"),
        ("english", "ENGLISH"),
        ("science", "SCIENCE"),
        ("social", "SOCIAL STUDIES"),
        ("ict", "ICT"),
        ("physics", "PHYSICS"),
        ("french", "FRENCH"),
        ("bumgt", "BUSINESS MANAGEMENT"),
        ("gov", "GOVERNMENT"),
        ("food", "FOOD 'N' NUTRITION"),
        ("gka", "GKA"),
        ("anihusb", "ANIMAL HUSBANDRY"),
    ]
    CATEGORY.sort(key=lambda x: x[1])

    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(300), nullable=False, info={"label": "Title"})
    classification_no = db.Column(
        db.String(10), unique=True, nullable=False, info={"label": "Classification No."}
    )
    author = db.Column(db.String(300), nullable=False, info={"label": "Author"})
    publication = db.Column(
        db.String(300), nullable=False, info={"label": "Publication"}
    )
    category = db.Column(
        ChoiceType(choices=CATEGORY), nullable=False, info={"label": "Category"}
    )
    download_link = db.Column(db.String(300), info={"label": "Book Download Link"})
    catalogue_no = db.Column(db.String(50), info={"label": "Catalogue No."})
    access_no = db.Column(db.Integer, nullable=False)
    date_recorded = db.Column(db.DateTime, nullable=False, default=dt.now())
    qty_added = db.Column(
        db.Integer, nullable=False, info={"label": "Quantity of Books"}
    )  # Number newly added
    qty_spoilt = db.Column(db.Integer, nullable=False)  # Number spoilt
    current_qty = db.Column(
        db.Integer, nullable=False
    )  # The current number in-stock (Current + Added) therefore Overall qty = current_qty + spoilt
    user_id = db.Column(db.Integer, db.ForeignKey(User.id))

    recorded_by = db.relationship(
        "User", backref=backref("books_recorded", uselist=False)
    )
    readers = db.relationship(
        "User", secondary=user_book, backref=db.backref("books_borrowed", lazy=True)
    )

    def __repr__(self):
        return f"<Books-id: {self.id}, Classification-No.: {self.classification_no}, Title: {self.title.rstrip()}>"
