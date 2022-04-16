from sqlalchemy.exc import IntegrityError

from .models import Books
from .. import db


def get_track(value):
    # Custom function to get a shorthand version of track
    # For example: if track value is GOLD, then the function will return GD
    new_text = str(value)
    shorthand = f"{new_text[0]}{new_text[-1]}".upper()
    return shorthand


def get_course(value):
    # Custom function to get a shorthand version of course
    # If the course value is one word, then the function will return the first 2 characters
    # or if the course value is two words, then the function will return the first character of each word
    # E.g.: BUSINESS = BU, GENERAL ARTS = GA
    new_text = str(value).split(' ', 1)
    shorthand = f"{new_text[0][0]}{new_text[1][0]}".upper() if len(new_text) == 2 else f"{new_text[0][0]}{new_text[0][1]}".upper()
    return shorthand


def process_data(file_data):
    parse_data(content=sorted(list(set(file_data)), key=lambda x: x[0]))


def parse_data(content: list[tuple]):
    books_list = [item for item in content]

    if len(books_list) != 0:
        books_recursive(books_list)


def books_recursive(data: list[tuple]):
    if len(data) > 100:
        add_books(books_data=data[:100])
        return books_recursive(data[100:])
    add_books(books_data=data)


def add_books(books_data: list[tuple]):
    books = Books()
    books_instances = []

    for item in books_data:
        book_classification_no = str(item[0]).lower()
        book_title = str(item[1]).lower()
        book_author = str(item[2]).lower()
        book_category = str(item[3]).lower()
        book_publication = str(item[4]).lower()
        book_qty_added = int(item[5])
        book_catalogue_no = str(item[6]).upper()
        book_download_link = str(item[7])

        books_exist = Books.query.filter(Books.classification_no == book_classification_no).first()
        if books_exist is not None:
            books_exist.current_qty = books_exist.current_qty + book_qty_added
            books_exist.classification_no = book_classification_no
            books_exist.title = book_title
            books_exist.author = book_author
            books_exist.category = book_category
            books_exist.publication = book_publication
            books_exist.qty_added = book_qty_added
            books_exist.catalogue_no = book_catalogue_no
            books_exist.download_link = book_download_link
            books_instances.append(books_exist)
        else:
            books.classification_no = book_classification_no
            books.title = book_title
            books.author = book_author
            books.category = book_category
            books.publication = book_publication
            books.qty_added = book_qty_added
            books.catalogue_no = book_catalogue_no
            books.download_link = book_download_link
            last_book = Books.query.order_by(Books.id.desc()).first()
            access_no = last_book.access_no + book_qty_added
            books.qty_spoilt, books.current_qty, books.access_no = (0, book_qty_added, access_no)
            books_instances.append(books)

    try:
        books.insert_many(books_instances)
    except IntegrityError:
        db.session.rollback()

