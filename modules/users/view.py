from functools import wraps

from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user
from pathlib import Path

from sqlalchemy.exc import IntegrityError

from .models import User, Class, Staff, Role
from .forms import StudentForm, TeacherForm, AdminForm


# Activation needed. Move from here to dashboard folder
def activation_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if not current_user.has_activated:
            return redirect(url_for("reset_password"))

        return f(*args, **kwargs)
    return wrap


static_path = Path('.').parent.absolute() / 'modules/static'
users_bp = Blueprint("users", __name__, url_prefix="/users", static_folder=static_path)


# CRUD for class records

# View to show user registration page
@users_bp.route("/register")
def user_index():
    context = {}
    user_log = True
    admin = True  # remove this when user login is implemented
    student_form = StudentForm()
    teacher_form = TeacherForm()
    admin_form = AdminForm()
    context.update(admin=admin, student_form=student_form, user_log=user_log,
                   teacher_form=teacher_form, admin_form=admin_form)
    return render_template("users/add.html", **context)


# View to create student accounts
@users_bp.route("/register/user/student", methods=['POST'])
def add_student_account():
    role = Role.query.filter(Role.purpose == 'student').first()
    form = StudentForm()
    student_user = User()
    form.populate_obj(student_user)
    try:
        if form.validate():
            print(form.validate_on_submit(), form.data)
            st_class, st_track = str(form.class_track.data).split("_", 1)
            student_class = Class.query.filter(
                Class.programme == form.programme.data,
                Class.year_group == form.year_group.data,
                Class.current_class == st_class,
                Class.track == st_track
            ).first()

            # Append user to role and class
            # TODO: student_user.password = form.password.data
            role.users.append(student_user)
            student_class.users.append(student_user)

            role.update()

    except IntegrityError:
        pass
    return redirect(url_for(".user_index"))


# View to create teacher accounts
@users_bp.route("/register/user/teacher", methods=['POST'])
def add_teacher_account():
    role = Role.query.filter(Role.purpose == 'teacher').first()
    form = TeacherForm()
    teacher_user = User()
    form.populate_obj(teacher_user)
    try:
        if form.validate():
            print(form.validate_on_submit(), form.data)
            teacher_dept = form.department.data
            # Append user to role and class
            # TODO: teacher_user.password = form.password.data
            role.users.append(teacher_user)
            teacher_dept.users.append(teacher_user)

            role.update()

    except IntegrityError:
        pass
    return redirect(url_for(".user_index"))


# View to create admin accounts
@users_bp.route("/register/user/admin", methods=['POST'])
def add_admin_account():
    role = Role.query.filter(Role.purpose == 'admin').first()
    form = AdminForm()
    admin_user = User()
    form.populate_obj(admin_user)
    try:
        if form.validate():
            print(form.validate_on_submit(), form.data)
            # Append user to role and class
            # TODO: admin_user.password = form.password.data
            role.users.append(admin_user)
            role.update()

    except IntegrityError:
        pass
    return redirect(url_for(".user_index"))

