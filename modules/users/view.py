from functools import wraps

from flask import Blueprint, redirect, url_for
from flask_login import current_user

from .models import User, Class, Staff, Role
# from project.modules.users.models import User, Class, Staff, Role


# Activation needed. Move from here to dashboard folder
def activation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.has_activated:
            return redirect(url_for("reset_password"))

        return f(*args, **kwargs)
    return wrap


users_bp = Blueprint("users", __name__, url_prefix="/users")


@users_bp.route("/user", defaults={"uid": 2})
def list_user(uid):
    return f"User is {uid}"
