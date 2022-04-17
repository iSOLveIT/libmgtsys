from flask import Blueprint


tracking_bp = Blueprint("tracking", __name__, url_prefix="/tracking")


# TODO: Add route for searching books borrowed. Results should filtered to books borrowed in the last 30 days
# TODO: Add route for searching users reading a specific book
# TODO: Add route for searching books borrowed by a user
# TODO: If user_id or name is not provided, then search all books borrowed by users.
#  Show the name & ID of user or book title on top of the results table when displaying results
# TODO: Use the tab navigation panel to show different search fields (search by book name and classification no.,
#  search by user name and sid, or show all results).
#  With the show all results, when the user clicks on the tab, it should send a request for all borrowed books.
