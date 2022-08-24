from flask import Blueprint
from flask import flash
from flask import redirect, escape
from flask import render_template
from flask import url_for
from flask import current_app
from flask import request
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from pathlib import Path

from project.helpers.security import get_safe_redirect

from project.modules.users.models import User
from .forms import LoginForm

# from .forms import RegistrationForm


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
    user_log = None
    login_form = LoginForm()
    context["form"] = login_form
    context["user_log"] = user_log
    if request.method == "POST":
        if not login_form.validate_on_submit():
            return render_template("login.html", **context)

        username = login_form.id.data
        password = login_form.password.data

        print(username, password)
        print(request.form)
        user = User.query.filter(User.id == username).first()
        if user is None or not user.check_password(password):
            flash(
                "Please ensure your User ID and password are correct", category="danger"
            )
            return redirect(url_for("auth.login"))
        login_user(user)

        # print(request.form)
        if "next" not in request.form:
            if current_user.is_admin:
                # next_url = url_for("dashboard.index")
                flash("You have logged in successfully!", category="success")
            else:
                # next_url = url_for('www.index')
                flash("You have logged in successfully!", category="success")

        else:
            if request.form["next"] == "":
                if current_user.is_admin:
                    # next_url = url_for("dashboard.index")
                    flash("You have logged in successfully!", category="success")
                else:
                    # next_url = url_for('www.index')
                    flash("You have logged in successfully!", category="success")
            else:
                if not current_user.is_admin:
                    # next_url = get_safe_redirect("/")
                    flash("You have logged in successfully!", category="success")
                    # return redirect(next_url)

                next_url = get_safe_redirect(request.form["next"])
                flash("You have logged in successfully!", category="success")
        # return redirect(next_url)
        return render_template("dashboard.html", **context)
    return render_template("login.html", **context)


# @auth_bp.route("/logout", methods=["GET"])
# @login_required
# def logout():
#     logout_user()

#     if "next" not in request.args or request.args.get("next") == "":
#         next_url = url_for("auth.login")
#         flash("Successfully logged out", category="success")
#     else:
#         flash("Successfully logged out", category="success")
#         redirect_url = url_for("auth.login", next=request.args.get("next"))
#         next_url = get_safe_redirect(redirect_url)

#     return redirect(next_url)
