from .models import User, Class, Staff, Role
from sqlalchemy.exc import IntegrityError

from .. import db


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
    role = Role.query.filter(Role.purpose == 'student').first()
    if role is None:
        pass

    user_instances = []
    for item in user_data:
        student_user = User()
        student_user.sid = str(item[1]).upper().replace("/", "_")
        student_user.name = str(item[2]).lower()
        student_user.gender = str(item[3]).upper()
        track, prog, year, _ = str(item[1]).upper().split("/", 3)

        try:
            student_class = Class.query.filter(
                Class.programme == prog,
                Class.year_group == str(2000 + int(year)),
                Class.current_class == str(item[5]).lower(),
                Class.track == track
            ).first()

            if student_class is None:
                continue

            student_class.users.append(student_user)  # Append user to class
            user_instances.append(student_user)

        except IntegrityError:
            db.session.rollback()
            continue

    role.users.extend(user_instances)
    role.insert_many(user_instances)
    print("Done")


def add_teachers(user_data: list[tuple]):
    pass
