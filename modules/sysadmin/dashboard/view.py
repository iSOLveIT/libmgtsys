from flask import Blueprint, request, redirect, render_template, url_for
from pathlib import Path
from sqlalchemy import or_

from project.modules.users.models import User, Class


static_path = Path('.').parent.absolute() / 'modules/static'
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/dashboard")


# NOTE: All post requests should refresh page

# Create and Read views for class records
@dashboard_bp.route('/admin')
def admin_dashboard():
    user_log = True
    context = {}
    admin = True    # remove this when user login is implemented
    total_users = User.query.filter(or_(User.role_id == 1, User.role_id == 2)).count()
    total_classes = Class.query.count()
    context.update(admin=admin, user_log=user_log, counts=[total_users, total_classes])
    return render_template("admin_dashboard.html", **context)
