# from datetime import datetime as dt

from flask import Blueprint, request, redirect, render_template, url_for, send_from_directory
from pathlib import Path
# from sqlalchemy import or_
from werkzeug.utils import secure_filename

from ... import allowed_file
from project.modules.users.models import User, StudentClass
from project.modules.books.models import Books
from project.modules.tracking.forms import SearchBooksForm
from .forms import BookTagForm

static_path = Path('.').parent.absolute() / 'modules/static'
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# VIEWS FOR THE ADMIN
# View for admin dashboard
@dashboard_bp.route('/admin')
def admin_dashboard():
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    total_users = User.query.count()
    total_classes = StudentClass.query.count()
    total_books = Books.query.count()
    search_form = SearchBooksForm()
    context.update(admin=admin, user_log=user_log, search_form=search_form,
                   counts=[total_users, total_classes, total_books])
    return render_template("admin_dashboard.html", **context)


# View to serve the Excel sample file so that they can be downloaded by users
@dashboard_bp.route('/admin/download_sample/<string:file_name>')
def download_sample_file(file_name):
    filename = secure_filename(file_name)
    if allowed_file(filename):
        return send_from_directory(static_path.joinpath("download"), filename)


# View for generating book tags
@dashboard_bp.route('/admin/book_tags', methods=["GET", "POST"])
def book_tags():
    cancel_print = request.args.get('cancel_print', default=False)
    user_log = True
    context = {}
    admin = True  # remove this when user login is implemented
    form = BookTagForm()
    """
        If request method is POST, then cancel_print == False so show the div with the generated tags output.
        If cancel_print == False and request.method is GET, then show the book tags page.
        Else if cancel_print == True and request.method is GET, then show the div with the book tags generator forms.
    """
    if request.method == 'POST' and form.validate():
        total_tags = (x + 3) // 2 if (x := int(form.total_tags.data)) % 2 != 0 else (x + 2) // 2
        counter = range(0, total_tags)
        bk_title, bk_class_no, bk_date = form.book_title.data, form.classification_no.data, form.tag_date.data
        context.update(cancel_print=cancel_print, bk_title=bk_title, bk_class_no=bk_class_no,
                       bk_date=bk_date, counter=counter)
        return render_template("others/tags_generated.html", **context)
    if not cancel_print:
        context.update(admin=admin, user_log=user_log, form=form)
        return render_template("others/book_tags.html", **context)
    context.update(cancel_print=cancel_print, form=form)
    return render_template("others/tags_generated.html", **context)


# VIEWS FOR USER (STUDENT and TEACHER)
# View for user dashboard
@dashboard_bp.route('/user/<string:user_id>')
def user_dashboard(user_id):
    user_log = True
    context = {}
    admin = False  # remove this when user login is implemented
    user_info = User.query.filter(User.sid == user_id).first()
    # total_classes = StudentClass.query.count()
    # total_books = Books.query.count()
    search_form = SearchBooksForm()
    context.update(admin=admin, user_log=user_log,
                   search_form=search_form, user_info=user_info)
    return render_template("user_dashboard.html", **context)


# View for user profile
@dashboard_bp.route('/user/profile')
def user_profile():
    user_log = True
    context = {}
    admin = False  # remove this when user login is implemented
    context.update(admin=admin, user_log=user_log)
    return render_template("others/user_profile.html", **context)

