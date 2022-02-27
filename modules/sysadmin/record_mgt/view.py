import re

from flask import Blueprint, request, redirect, render_template, url_for
from pathlib import Path
from sqlalchemy.exc import IntegrityError

from project.modules.users.models import User, Class, Role, Staff
from .forms import AddClassForm, AddStaffForm, AddRoleForm, SearchStaffForm, SearchClassForm
# from project.helpers.security import get_safe_redirect


static_path = Path('.').parent.absolute() / 'modules/static'
record_mgt_bp = Blueprint("record_mgt", __name__, url_prefix="/record_mgt", static_folder=static_path)


# CRUD for class records

# View to show class page
@record_mgt_bp.route('/class')
def class_index():
    context = {}
    admin = True    # remove this when user login is implemented
    form = AddClassForm()
    searchform = SearchClassForm()
    context.update(locals())
    return render_template("records_mgt/class.html", **context)


# View to Create class records
@record_mgt_bp.route('/class/add_class', methods=['POST'])
def add_class():
    form = AddClassForm()
    if not form.validate():
        # msg = "Form details were incorrect!"
        return redirect(url_for(".class_index"))
    tag = f"{form.programme.data}{str(form.current_class.data).upper()}{form.track.data}{form.year_group.data}"

    student_class = Class()
    form.populate_obj(student_class)
    student_class.class_tag = tag
    try:
        student_class.update()
        # msg = "Created class details successfully"
    except IntegrityError:
        # msg = "Class details already exists!"
        pass
    return redirect(url_for(".class_index"))


# View to Edit class records
@record_mgt_bp.route('/class/edit_class/<class_id>', methods=['GET', 'POST'])
def edit_class(class_id):
    view = "class"
    context = {}
    admin = True  # remove this when user login is implemented
    class_id = class_id
    class_record = Class.query.get(class_id)
    form = AddClassForm(obj=class_record)
    if request.method == 'POST' and form.validate():
        tag = f"{form.programme.data}{str(form.current_class.data).upper()}{form.track.data}{form.year_group.data}"
        class_record = Class.query.filter(Class.id == class_id).with_for_update().first()
        form.populate_obj(class_record)
        class_record.class_tag = tag
        try:
            class_record.update()
            # msg = "Updated class details successfully"
        except IntegrityError:
            # msg = "Class details already exists!"
            pass
        return redirect(url_for(".class_index"))
    context.update(locals())
    return render_template("records_mgt/edit_record.html", **context)


# View to Search class records
@record_mgt_bp.route('/class/search_class')
def search_class():
    view = "class"
    context = {}
    prog = request.args.get("programme", default=None)
    track = request.args.get("track", default=None)
    yr_grp = request.args.get("year_group")

    check_yr_grp = re.search(r"^\d{4}$", yr_grp)

    if check_yr_grp is not None:
        class_records = Class.query.filter(
            Class.programme == prog,
            Class.track == track,
            Class.year_group == yr_grp).all()
        context.update(class_records=class_records, view=view)
    return render_template("records_mgt/records_output.html", **context)


# View to Delete class records
@record_mgt_bp.route('/class/delete_class/<class_id>', methods=['DELETE'])
def delete_class(class_id):
    view = "class"
    # admin = True  # remove this when user login is implemented
    class_record = Class.query.filter(Class.id == class_id).with_for_update().first()
    prog = class_record.programme
    yr_grp = class_record.year_group
    track = class_record.track
    class_record.delete()

    context = {}
    class_records = Class.query.filter(
        Class.programme == prog,
        Class.track == track,
        Class.year_group == yr_grp).all()
    context.update(class_records=class_records, view=view)
    # msg = "Deleted class details successfully!"
    return render_template("records_mgt/records_output.html", **context)


# CRUD for staff records

# View to show staff page
@record_mgt_bp.route('/staff')
def staff_index():
    context = {}
    admin = True    # remove this when user login is implemented
    form = AddStaffForm()
    searchform = SearchStaffForm()
    context.update(locals())
    return render_template("records_mgt/staff.html", **context)


# View to Create staff records
@record_mgt_bp.route('/staff/add_staff', methods=['POST'])
def add_staff():
    form = AddStaffForm()
    if not form.validate():
        # msg = "Form details were incorrect!"
        return redirect(url_for(".staff_index"))
    teacher_dept = Staff()
    form.populate_obj(teacher_dept)
    try:
        teacher_dept.update()
        # msg = "Created staff details successfully"
    except IntegrityError:
        # msg = "Staff details already exists!"
        pass
    return redirect(url_for(".staff_index"))


# View to Edit staff records
@record_mgt_bp.route('/staff/edit_staff/<staff_id>', methods=['GET', 'POST'])
def edit_staff(staff_id):
    view = "staff"
    context = {}
    admin = True  # remove this when user login is implemented
    staff_id = staff_id
    staff_record = Staff.query.get(staff_id)
    form = AddStaffForm(obj=staff_record)
    if request.method == 'POST' and form.validate():
        # prevent changes in selected row until you commit changes to DB
        staff_record = Staff.query.filter(Staff.id == staff_id).with_for_update().first()
        form.populate_obj(staff_record)
        try:
            staff_record.update()
            # msg = "Created staff details successfully"
        except IntegrityError:
            # msg = "Staff details already exists!"
            pass
        return redirect(url_for(".staff_index"))
    context.update(locals())
    # msg = "Updated staff details successfully"
    return render_template("records_mgt/edit_record.html", **context)


# View to Search staff records
@record_mgt_bp.route('/staff/search_staff')
def search_staff():
    view = "staff"
    context = {}
    dept = int(request.args.get("department", default=None))

    staff_record = Staff.query.filter(Staff.id == dept).first()
    context.update(dept_record=staff_record, view=view)
    return render_template("records_mgt/records_output.html", **context)


# View to Delete staff records
@record_mgt_bp.route('/staff/delete_staff/<staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    view = "staff"
    # admin = True  # remove this when user login is implemented
    staff_record = Staff.query.filter(Staff.id == staff_id).with_for_update().first()
    dept = staff_record.department
    staff_record.delete()

    context = {}
    staff_record = Staff.query.filter(Staff.department == dept).first()
    # msg = "Deleted staff details successfully"
    context.update(dept_record=staff_record, view=view)
    return render_template("records_mgt/records_output.html", **context)


# CRUD for roles records

# View to show roles page
@record_mgt_bp.route('/role')
def role_index():
    context = {}
    admin = True    # remove this when user login is implemented
    form = AddRoleForm()
    role_records = Role.query.all()
    context.update(locals())
    return render_template("records_mgt/role.html", **context)


# View to Create role records
@record_mgt_bp.route('/role/add_role', methods=['POST'])
def add_role():
    form = AddRoleForm()
    if form.validate():
        account_type = Role()
        form.populate_obj(account_type)
        if form.purpose.data == 'admin':
            account_type.permission_level = True
        try:
            account_type.update()
            # msg = "Updated role details successfully"
        except IntegrityError:
            # msg = "Role details already exists!"
            pass

    view = "role"
    context = {}
    role_records = Role.query.all()
    context.update(role_records=role_records, view=view)
    # msg = "Form details were incorrect!"
    return render_template("records_mgt/records_output.html", **context)


# View to Edit role records
@record_mgt_bp.route('/role/edit_role/<role_id>', methods=['GET', 'POST'])
def edit_role(role_id):
    view = "role"
    context = {}
    admin = True  # remove this when user login is implemented
    role_id = role_id
    role_record = Role.query.get(role_id)
    form = AddRoleForm(obj=role_record)
    if request.method == 'POST' and form.validate():
        # prevent changes in selected row until you commit changes to DB
        role_record = Role.query.filter(Role.id == role_id).with_for_update().first()
        form.populate_obj(role_record)
        role_record.permission_level = False
        if form.purpose.data == 'admin':
            role_record.permission_level = True
        try:
            role_record.update()
            # msg = "Updated role details successfully"
        except IntegrityError:
            # msg = "Role details already exists!"
            pass
        return redirect(url_for(".role_index"))
    context.update(locals())
    return render_template("records_mgt/edit_record.html", **context)


# View to Delete role records
@record_mgt_bp.route('/role/delete_role/<role_id>', methods=['DELETE'])
def delete_role(role_id):
    view = "role"
    # admin = True  # remove this when user login is implemented
    role_record = Role.query.filter(Role.id == role_id).with_for_update().first()
    role_record.delete()

    context = {}
    role_records = Role.query.all()
    context.update(role_records=role_records, view=view)
    # msg = "Deleted role details successfully"
    return render_template("records_mgt/records_output.html", **context)

