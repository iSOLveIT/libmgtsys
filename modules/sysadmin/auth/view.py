from functools import wraps

from flask import Blueprint, flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from pathlib import Path

from project.helpers.security import get_safe_redirect

from project.modules.users.models import User
from .forms import LoginForm

# from .forms import RegistrationForm

def admin_only_route(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated and current_user.is_admin:
            return url_for("dashboard.user_dashboard", user_id=current_user.sid)
        return func(*args, **kwargs)

    return decorated_view

static_path = Path(".").parent.absolute() / "modules/static"
auth_bp = Blueprint("auth", __name__, url_prefix="/auth", static_folder=static_path)

#
# @auth_bp.route("/register", methods=["GET", "POST"])
# def register():
#     context = {}
#     reg_form = RegistrationForm()
#
#     if reg_form.validate_on_submit():
#         email = reg_form.email.data
#         password = reg_form.password.data
#         user = User.create(email=email, password=password, is_admin=False)
#         login_user(user)
#
#         is_disabled = False
#
#         if "EMAIL_CONFIRMATION_DISABLED" in current_app.config:
#             is_disabled = current_app.config["EMAIL_CONFIRMATION_DISABLED"]
#
#         if is_disabled is True:
#             user.is_email_confirmed = True
#             user.email_confirm_date = datetime.datetime.now()
#             user.update()
#         else:
#             token = user.generate_confirmation_token()
#             template = "auth/emails/activate_user"
#             subject = "Please confirm your email"
#             context.update({"token": token, "user": user})
#             send_async_email(email, subject, template, **context)
#             flash(
#                 notify_success("A confirmation email has been sent via email.")
#             )
#
#         return redirect(url_for("www.index"))
#
#     context["form"] = reg_form
#     return render_template("auth/register.html", **context)


@auth_bp.route("/", methods=["GET", "POST"])
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    context = {}
    login_form = LoginForm()
    context["form"] = login_form
    if request.method == "POST":
        if not login_form.validate_on_submit():
            flash(
                "Please ensure your User ID and password are correct", category="danger"
            )
            return redirect(url_for("auth.login"))

        username = str(login_form.sid.data).upper().replace("/", "_")
        password = login_form.show_pswd.data

        user: User = User.query.filter(User.sid == username).first()
        if user is None or not user.check_password(password):
            flash(
                "Please ensure your User ID and password are correct", category="danger"
            )
            return redirect(url_for("auth.login"))
        user.authenticated = True
        login_user(user)

        if "next" not in request.form:
            if current_user.is_admin:
                next_url = url_for("dashboard.admin_dashboard")
            else:
                next_url = url_for("dashboard.user_dashboard", user_id=current_user.sid)
        else:
            if len(request.form["next"]) <= 0:
                if current_user.is_admin:
                    next_url = url_for("dashboard.admin_dashboard")
                else:
                    next_url = url_for("dashboard.user_dashboard", user_id=current_user.sid)

            next_url = get_safe_redirect(request.form["next"])
            flash("You have logged in successfully!", category="success")
        return redirect(next_url)
    return render_template("login.html", **context)


@auth_bp.route("/logout", methods=["GET"])
@login_required
def logout():
    user: User = current_user
    user.authenticated = False
    logout_user()

    if "next" not in request.args or len(request.form["next"]) <= 0:
        next_url = url_for("auth.login")
        flash("Successfully logged out", category="success")
    else:
        flash("Successfully logged out", category="success")
        redirect_url = url_for("auth.login", next=request.args.get("next"))
        next_url = get_safe_redirect(redirect_url)

    return redirect(next_url)
