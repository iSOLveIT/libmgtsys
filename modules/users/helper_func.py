import random

from sqlalchemy.exc import IntegrityError

from .. import db
from .models import User, StudentClass, Staff, Role


def pswd_gen():
    content = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789@#$"
    generated_list = random.choices(content, k=4)
    return "SWESCO_" + "".join(generated_list)


def process_data(file_data):
    parse_data(content=sorted(list(set(file_data)), key=lambda x: x[1]))


def parse_data(content: list[tuple]):
    student_account = [item for item in content if item[0].lower() == "student"]
    teacher_account = [item for item in content if item[0].lower() == "teacher"]

    if len(student_account) != 0:
        student_recursive(student_account)
    if len(teacher_account) != 0:
        teacher_recursive(teacher_account)


def student_recursive(data: list[tuple]):
    if len(data) > 100:
        add_students(user_data=data[:100])
        return student_recursive(data[100:])
    add_students(user_data=data)


def teacher_recursive(data: list[tuple]):
    if len(data) > 100:
        add_teachers(user_data=data[:100])
        return teacher_recursive(data[100:])
    add_teachers(user_data=data)


def add_students(user_data: list[tuple]):
    role = Role.query.filter(Role.purpose == "student").first()
    if role is None:
        pass

    user_instances = []
    for item in user_data:
        user_exist = User.query.filter(
            User.sid == str(item[1]).upper().replace("/", "_")
        ).first()
        if user_exist is not None:
            continue

        student_user = User()
        student_user.sid = str(item[1]).upper().replace("/", "_")
        student_user.name = str(item[2]).lower().rstrip()
        student_user.gender = str(item[3]).upper().rstrip()
        student_user.password = pswd_gen()
        track, prog, year, _ = str(item[1]).upper().split("/", 3)

        student_class = StudentClass.query.filter(
            StudentClass.programme == prog,
            StudentClass.year_group == str(2000 + int(year)),
            StudentClass.current_class == str(item[5]).lower(),
            StudentClass.track == track,
        ).first()

        if student_class is None:
            continue

        student_class.users.append(student_user)  # Append user to class
        user_instances.append(student_user)
    try:
        role.users.extend(user_instances)
        role.insert_many(user_instances)
    except IntegrityError:
        db.session.rollback()


def add_teachers(user_data: list[tuple]):
    role = Role.query.filter(Role.purpose == "teacher").first()
    if role is None:
        pass

    user_instances = []
    for item in user_data:
        user_exist = User.query.filter(
            User.sid == str(item[1]).upper().replace("/", "_")
        ).first()
        if user_exist is not None:
            continue

        teacher_user = User()
        teacher_user.sid = str(item[1]).upper().replace("/", "_")
        teacher_user.name = str(item[2]).lower()
        teacher_user.gender = str(item[3]).upper()
        teacher_user.password = pswd_gen()
        dept = str(item[4]).capitalize()

        teacher_dept = Staff.query.filter(Staff.department == dept).first()

        if teacher_dept is None:
            continue

        teacher_dept.users.append(teacher_user)  # Append user to staff group
        user_instances.append(teacher_user)
    try:
        role.users.extend(user_instances)
        role.insert_many(user_instances)
    except IntegrityError:
        db.session.rollback()
