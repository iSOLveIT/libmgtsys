from .models import User, Class, Role, Staff
from project.modules import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired, Length, DataRequired
# from flask_wtf.file import FileField
from wtforms.fields import SelectField, IntegerField, StringField
from string import ascii_uppercase

gd_cl_track = [f"{i}_GOLD" for i in ascii_uppercase]
gn_cl_track = [f"{i}_GREEN" for i in ascii_uppercase]


class StudentForm(ModelForm):
    """
    StudentForm - Form for adding students

    """
    id = StringField(u"Student ID", validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
                     render_kw={'class': "form-control", 'placeholder': "10087872"})

    class Meta:
        model = User
        only = ['id', 'name', 'gender']
        field_args = {

            'name': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'Lastname Firstname, e.g. Asebu Sophia'
                }
            },
            'gender': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control gender',
                    'id': 's_gender'
                }
            }
        }

    programme = SelectField(u"Programme", choices=Class.COURSES, validators=[InputRequired(), DataRequired()],
                            render_kw={'class': "form-control programme"})
    year_group = IntegerField(u"Admission Year", validators=[InputRequired(), DataRequired(), Length(min=4, max=4)],
                              render_kw={'class': 'form-control',
                                         'placeholder': 'Year enrolled, e.g. 2016',
                                         'pattern': r'^\d{4}$',
                                         'title': 'Year should be 4 digits'})
    class_track = SelectField(u"Class & Track", choices=[(ct.lower(), ct) for ct in gd_cl_track + gn_cl_track],
                              validators=[InputRequired(), DataRequired()],
                              render_kw={'class': 'form-control', 'id': 'current_class'})


class TeacherForm(ModelForm):
    """
    TeacherForm - Form for adding teachers

    """

    class Meta:
        model = User
        only = ['id', 'name', 'gender']
        field_args = {
            'name': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'Lastname Firstname, e.g. Asebu Sophia'
                }
            },
            'gender': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control gender',
                    'id': 't_gender'
                }
            }
        }

    id = StringField(u"Staff ID", validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
                     render_kw={'class': "form-control", 'placeholder': "TA10218761"})
    department = QuerySelectField(
        'Department:',
        validators=[InputRequired()],
        query_factory=lambda: Staff.query.order_by(Staff.department).all(),
        get_label="department",
        render_kw={
            'class': "form-control dept"
        }
    )


class AdminForm(ModelForm):
    """
    AdminForm - Form for adding administrators

    """

    class Meta:
        model = User
        only = ['id', 'name', 'password', 'gender']
        field_args = {
            'password': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': ''
                }
            },
            'name': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'Lastname Firstname, e.g. Asebu Sophia'
                }
            },
            'gender': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control gender',
                    'id': 'a_gender'
                }
            }
        }

    id = StringField(u"Admin ID", validators=[InputRequired(), DataRequired(), Length(min=10, max=30)],
                     render_kw={'class': "form-control", 'placeholder': "AD10318723"})
