from flask import Blueprint, request, redirect, render_template, url_for
from pathlib import Path

from project.modules.users.models import User, Class, Role, Staff
from .forms import AddClassForm, AddStaffForm, AddRoleForm, SearchStaffForm, SearchClassForm
# from project.helpers.security import get_safe_redirect


static_path = Path('.').parent.absolute() / 'modules/static'
record_mgt_bp = Blueprint("record_mgt", __name__, url_prefix="/record_mgt", static_folder=static_path)


# TODO: CRUD for class records
# NOTE: All post requests should refresh page

# Create and Read views for class records
@record_mgt_bp.route('/class')
def class_index():
    context = {}
    admin = True    # remove this when user login is implemented
    form = AddClassForm()
    context.update(locals())
    return render_template("records_mgt/class.html", **context)


@record_mgt_bp.route('/add_class', methods=['POST'])
def add_class():
    form = AddClassForm()
    admission_yr: str = str(request.form.get('year_group')).split('-', 1)[0]
    student_class = Class()

    form.populate_obj(student_class)
    student_class.year_group = admission_yr
    student_class.update()
    return redirect(url_for(".class_index"))


@record_mgt_bp.route('/edit_class', methods=['POST'])
def edit_class():
    pass


@record_mgt_bp.route('/search_class')
def search_class():
    pass


@record_mgt_bp.route('/delete_class', methods=['DELETE'])
def delete_class():
    pass


# TODO: CRUD for staff records

# TODO: CRUD for roles records
