from flask import Blueprint


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/user", defaults={"id": 2})
def list_user(id):
    return f"User is {id}"
