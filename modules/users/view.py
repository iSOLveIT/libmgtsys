from flask import Blueprint

from .models import User, Class, Staff, Role
# from project.modules.users.models import User, Class, Staff, Role


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/user", defaults={"uid": 2})
def list_user(uid):
    return f"User is {uid}"
