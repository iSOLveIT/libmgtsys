from string import ascii_uppercase

from .models import User, Staff
from project.modules import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired, Length, DataRequired

# from flask_wtf.file import FileField
from wtforms.fields import SelectField, StringField, SearchField


class StudentForm(ModelForm):
    """
    StudentForm - Form for adding students

    """

    class Meta:
        model = User
        only = ["sid", "name", "gender"]
        field_args = {
            "name": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control",
                    "placeholder": "Lastname Firstname, e.g. Asebu Sophia",
                }
            },
            "gender": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control gender",
                    "id": "s_gender",
                }
            },
        }

    sid = StringField(
        "Student ID",
        validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
        render_kw={"class": "form-control", "placeholder": "GD/GA/19/116"},
    )
    current_class = SelectField(
        "Current Class",
        choices=[(ct.lower(), ct) for ct in ascii_uppercase],
        validators=[InputRequired(), DataRequired()],
        render_kw={"class": "form-control", "id": "current_class"},
    )


class TeacherForm(ModelForm):
    """
    TeacherForm - Form for adding teachers

    """

    class Meta:
        model = User
        only = ["sid", "name", "gender"]
        field_args = {
            "name": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control",
                    "placeholder": "Lastname Firstname, e.g. Asebu Sophia",
                }
            },
            "gender": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control gender",
                    "id": "t_gender",
                }
            },
        }

    sid = StringField(
        "Staff ID",
        validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
        render_kw={"class": "form-control", "placeholder": "TA10218761"},
    )
    department = QuerySelectField(
        "Department:",
        validators=[InputRequired()],
        query_factory=lambda: Staff.query.order_by(Staff.department).all(),
        get_label="department",
        render_kw={"class": "form-control dept"},
    )


class AdminForm(ModelForm):
    """
    AdminForm - Form for adding administrators

    """

    class Meta:
        model = User
        only = ["sid", "name", "password", "gender"]
        field_args = {
            "password": {"render_kw": {"autocomplete": "off", "required": ""}},
            "name": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control",
                    "placeholder": "Lastname Firstname, e.g. Asebu Sophia",
                }
            },
            "gender": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control gender",
                    "id": "a_gender",
                }
            },
        }

    sid = StringField(
        "Admin ID",
        validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
        render_kw={"class": "form-control", "placeholder": "AD10318723"},
    )


class EditAdminForm(ModelForm):
    """
    AdminForm - Form for adding administrators

    """

    class Meta:
        model = User
        only = ["sid", "name", "gender"]
        field_args = {
            "name": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control",
                    "placeholder": "Lastname Firstname, e.g. Asebu Sophia",
                }
            },
            "gender": {
                "render_kw": {
                    "autocomplete": "off",
                    "required": "",
                    "class": "form-control gender",
                    "id": "a_gender",
                }
            },
        }

    sid = StringField(
        "Admin ID",
        validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
        render_kw={"class": "form-control", "placeholder": "AD10318723"},
    )


class SearchUserForm(ModelForm):
    """
    SearchUserForm - Form for searching users

    """

    search_term = SearchField(
        "Keyword",
        validators=[InputRequired(), DataRequired(), Length(min=4, max=30)],
        render_kw={
            "autocomplete": "off",
            "required": "",
            "class": "form-control",
            "placeholder": "Type name or user ID",
            "hx-post": "/users/list",
            "hx-trigger": "keyup changed delay:500ms, search",
            "hx-target": "#results_box",
            "hx-swap": "outerHTML",
        },
    )
