from sqlalchemy.exc import IntegrityError

from ...users.models import StudentClass
from ... import db


def get_track(value):
    # Custom function to get a shorthand version of track
    # For example: if track value is GOLD, then the function will return GD
    new_text = str(value)
    shorthand = f"{new_text[0]}{new_text[-1]}".upper()
    return shorthand


def get_course(value):
    # Custom function to get a shorthand version of course
    # If the course value is one word, then the function will return the first 2 characters
    # or if the course value is two words, then the function will return the first character of each word
    # E.g.: BUSINESS = BU, GENERAL ARTS = GA
    new_text = str(value).split(' ', 1)
    shorthand = f"{new_text[0][0]}{new_text[1][0]}".upper() if len(new_text) == 2 else f"{new_text[0][0]}{new_text[0][1]}".upper()
    return shorthand


def process_data(file_data):
    parse_data(content=sorted(list(set(file_data)), key=lambda x: x[0]))


def parse_data(content: list[tuple]):
    student_class = [item for item in content]

    if len(student_class) != 0:
        class_recursive(student_class)


def class_recursive(data: list[tuple]):
    if len(data) > 100:
        add_classes(class_data=data[:100])
        return class_recursive(data[100:])
    add_classes(class_data=data)


def add_classes(class_data: list[tuple]):
    student_class = StudentClass()
    student_class_instances = []

    for item in class_data:
        course = get_course(str(item[0]))
        track = get_track(str(item[1]))
        admission_year = str(item[2])
        current_class = str(item[3]).lower()
        tag = f"{course}{current_class.upper()}{track}{admission_year}"

        class_exist = StudentClass.query.filter(StudentClass.class_tag == tag).first()
        if class_exist is not None:
            continue

        student_class.programme = course
        student_class.track = track
        student_class.current_class = current_class
        student_class.year_group = admission_year
        student_class.class_tag = tag
        student_class_instances.append(student_class)

    try:
        student_class.insert_many(student_class_instances)
    except IntegrityError:
        db.session.rollback()

