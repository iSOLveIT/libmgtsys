# from datetime import datetime as dt

from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
    send_from_directory,
    flash
)
from pathlib import Path

from sqlalchemy import or_, desc, and_
from werkzeug.utils import secure_filename

from ... import allowed_file
from project.modules.users.models import User, StudentClass, Role, Staff
from project.modules.books.models import Books, UserBooksHistory
from project.modules.tracking.forms import SearchAvailableBooksForm
from project.modules.books.forms import SearchBooksForm
from .forms import BookTagForm, ReportForm

static_path = Path(".").parent.absolute() / "modules/static"
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


@dashboard_bp.route("/")
def dashboard():
    return redirect(url_for("auth.login"))


# VIEWS FOR THE ADMIN
# View for admin dashboard
@dashboard_bp.route("/admin")
def admin_dashboard():
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    total_users = User.query.count()
    total_books = Books.query.count()
    total_borrowed_books = Books.query.filter(Books.readers).count()
    total_classes = StudentClass.query.count()
    search_form = SearchBooksForm()
    context.update(
        admin=admin,
        user_log=user_log,
        search_form=search_form,
        counts=[
            total_users,
            total_books,
            total_classes,
            total_borrowed_books,
        ],
    )
    return render_template("admin_dashboard.html", **context)


# View to serve the Excel sample file so that they can be downloaded by users
@dashboard_bp.route("/admin/download_sample/<string:file_name>")
def download_sample_file(file_name):
    filename = secure_filename(file_name)
    if allowed_file(filename):
        return send_from_directory(static_path.joinpath("download"), filename)


# View for generating book tags
@dashboard_bp.route("/admin/book_tags", methods=["GET", "POST"])
def book_tags():
    cancel_print = request.args.get("cancel_print", default=False)
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    form = BookTagForm()
    """
        If request method is POST, then cancel_print == False so show the div with the generated tags output.
        If cancel_print == False and request.method is GET, then show the book tags page.
        Else if cancel_print == True and request.method is GET, then show the div with the book tags generator forms.
    """
    if request.method == "POST" and form.validate():
        total_tags = (
            (x + 3) // 2 if (x := int(form.total_tags.data)) % 2 != 0 else (x + 2) // 2
        )
        counter = range(0, total_tags)
        bk_sch, bk_title, bk_class_no, bk_date = (
            form.sch_name.data,
            form.book_title.data,
            form.classification_no.data,
            form.tag_date.data,
        )
        context.update(
            cancel_print=cancel_print,
            bk_title=bk_title,
            bk_class_no=bk_class_no,
            bk_date=bk_date,
            bk_sch=bk_sch,
            counter=counter,
        )
        return render_template("others/tags_generated.html", **context)
    if not cancel_print:
        context.update(admin=admin, user_log=user_log, form=form)
        return render_template("others/book_tags.html", **context)
    context.update(cancel_print=cancel_print, form=form)
    return render_template("others/tags_generated.html", **context)


# View for admin reports
@dashboard_bp.route("/admin/reports", methods=["GET", "POST"])
def generate_reports():
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    report_type = request.args.get("select_report", default=None, type=str)
    report_form = ReportForm()
    context.update(admin=admin, user_log=user_log, report_form=report_form)

    if report_type is None:
        return render_template("others/reports.html", **context)

    report_type_context = {}
    if report_type == "users":
        user_roles = Role.query.all()
        report_type_context.update(roles=user_roles, report_type=report_type)
        return render_template("others/report_type.html", **report_type_context)
    elif report_type == "books":
        book_category = Staff.query.all()
        report_type_context.update(categories=book_category, report_type=report_type)
        return render_template("others/report_type.html", **report_type_context)
    elif report_type == "books_issued":
        book_category = Staff.query.all()
        report_type_context.update(categories=book_category, report_type=report_type)
        return render_template("others/report_type.html", **report_type_context)
    else:
        return render_template("others/report_type.html", **report_type_context)


@dashboard_bp.route("/admin/print_reports", methods=["GET", "POST"])
def print_reports():
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    cancel_print = request.args.get("cancel_print", default=None, type=str)
    report_form = ReportForm()
    report_type = report_form.select_report.data or None
    if report_type == "users":
        user_roles = Role.query.all()
        report_form.report_type.choices = [(item.id, str(item.purpose).capitalize()) for item in user_roles]
    elif report_type == "books" or report_type == "books_issued":
        book_category = Staff.query.all()
        report_form.report_type.choices = [(str(item.department).lower(), item.department) for item in book_category]
    context.update(admin=admin, user_log=user_log, report_form=report_form)

    if cancel_print:
        return render_template("others/report_generated.html", **context)

    if not report_form.validate():
        flash("Report could not be generated.", "danger")
        return render_template("others/report_generated.html", **context)

    generate_report_for = report_form.select_report.data
    generate_report_type = report_form.report_type.data
    report_start_date = report_form.start_date.data
    report_end_date = report_form.end_date.data

    if generate_report_for == "users":
        users_results = User.query.filter(
            and_(
                User.role_id == generate_report_type,
                User.date_registered.between(report_start_date, report_end_date)
            )
        ).all()
        context.update(users_results=users_results, report_type=generate_report_for)
        return render_template("others/report_generated.html", **context)
    elif generate_report_for == "books":
        books_results = Books.query.filter(
            and_(
                Books.category == generate_report_type,
                Books.date_recorded.between(report_start_date, report_end_date)
            )
        ).all()
        context.update(books_results=books_results, report_type=generate_report_for)
        return render_template("others/report_generated.html", **context)
    elif generate_report_for == "books_issued":
        books_issued_results = UserBooksHistory.query.filter(
            UserBooksHistory.date_borrowed.between(report_start_date, report_end_date)
        ).all()
        context.update(books_issued_results=books_issued_results, report_type=generate_report_for,
                       category=str(generate_report_type).upper())
        return render_template("others/report_generated.html", **context)
    else:
        flash("Report could not be generated.", "danger")
        return render_template("others/report_type.html", **context)


# VIEWS FOR USER (STUDENT and TEACHER)
# View for user dashboard
@dashboard_bp.route("/user/<string:user_id>")
def user_dashboard(user_id):
    user_log = True
    context = {}
    admin = False  # remove this when user login is implemented
    user_info = User.query.filter(User.sid == user_id).first()
    total_books_borrowed = UserBooksHistory.query.filter(
        UserBooksHistory.user_id == user_info.id
    ).count()
    search_form = SearchAvailableBooksForm()
    context.update(
        admin=admin,
        user_log=user_log,
        books_borrowed=total_books_borrowed,
        search_form=search_form,
        user_info=user_info,
    )
    return render_template("user_dashboard.html", **context)


# View for user profile
@dashboard_bp.route("/user/profile")
def user_profile():
    user_log = True
    context = {}
    admin = False  # remove this when user login is implemented
    context.update(admin=admin, user_log=user_log)
    return render_template("others/user_profile.html", **context)
