from flask import Blueprint, request, redirect, render_template, url_for, send_from_directory
from pathlib import Path
# from sqlalchemy import or_
from werkzeug.utils import secure_filename

from project.modules.users.models import User, StudentClass
from project.modules.books.models import Books
from ... import allowed_file


static_path = Path('.').parent.absolute() / 'modules/static'
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# Create and Read views for class records
@dashboard_bp.route('/admin')
def admin_dashboard():
    user_log = True
    context = {}
    admin = True    # remove this when user login is implemented
    total_users = User.query.count()
    total_classes = StudentClass.query.count()
    total_books = Books.query.count()
    context.update(admin=admin, user_log=user_log, counts=[total_users, total_classes, total_books])
    return render_template("admin_dashboard.html", **context)


# View to serve the Excel sample file so that they can be downloaded by users
@dashboard_bp.route('/download_sample/<string:file_name>')
def download_sample_file(file_name):
    filename = secure_filename(file_name)
    if allowed_file(filename):
        return send_from_directory(static_path.joinpath("download"), filename)
