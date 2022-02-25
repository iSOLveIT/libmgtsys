from flask import Blueprint, request, redirect, render_template, url_for
from pathlib import Path

from project.modules.users.models import User, Class, Role, Staff
from .forms import AddClassForm, AddStaffForm, AddRoleForm, SearchStaffForm, SearchClassForm
# from project.helpers.security import get_safe_redirect


static_path = Path('.').parent.absolute() / 'modules/static'
record_mgt_bp = Blueprint("record_mgt", __name__, url_prefix="/record_mgt", static_folder=static_path)


# CRUD for class records

# Create and Read views for class records
@record_mgt_bp.route('/class', methods=['GET', 'POST'])
def class_index():
    context = {}
    admin = True    # remove this when user login is implemented
    form = AddClassForm()
    searchform = SearchClassForm()
    if request.method == 'POST' and searchform.validate():
        class_records = Class.query.filter(
            Class.programme == searchform.programme.data,
            Class.year_group == str(searchform.year_group.data)).all()
    context.update(locals())
    return render_template("records_mgt/class.html", **context)


@record_mgt_bp.route('/add_class', methods=['POST'])
def add_class():
    form = AddClassForm()
    if not form.validate():
        return redirect(url_for(".class_index"))
    student_class = Class()
    form.populate_obj(student_class)
    student_class.update()
    return redirect(url_for(".class_index"))


@record_mgt_bp.route('/edit_class/<class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    context = {}
    admin = True  # remove this when user login is implemented
    class_id = class_id
    class_record = Class.query.get(class_id)
    form = AddClassForm(obj=class_record)
    if request.method == 'POST' and form.validate():
        form.populate_obj(class_record)
        class_record.update()
        return redirect(url_for(".class_index"))
    context.update(locals())
    return render_template("records_mgt/edit_record.html", **context)


@record_mgt_bp.route('/search_class')
def search_class():
    prog = request.args.get("programme")
    yr_grp = request.args.get("year_group")

    context = {}
    class_records = Class.query.filter(
        Class.programme == prog,
        Class.year_group == str(yr_grp)).all()
    context.update(class_records=class_records)
    return render_template("records_mgt/records_output.html", **context)


@record_mgt_bp.route('/delete_class/<class_id>', methods=['DELETE'])
def delete_class(class_id):

    # admin = True  # remove this when user login is implemented
    class_record = Class.query.get(class_id)
    prog = class_record.programme
    yr_grp = class_record.year_group
    class_record.delete()

    context = {}
    class_records = Class.query.filter(
        Class.programme == prog,
        Class.year_group == str(yr_grp)).all()
    context.update(class_records=class_records)
    return render_template("records_mgt/records_output.html", **context)


# TODO: CRUD for staff records

# TODO: CRUD for roles records
