from project.modules.users.models import User, Class, Role, Staff
from project.modules import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired


# Forms for class records

class AddClassForm(ModelForm):
    """
    AddClass - Form for adding classes

    """
    class Meta:
        model = Class
        only = ['programme', 'current_class', 'track']
        field_args = {
            'programme': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control programme'
                }
            },
            'track': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control',
                    'id': 'track'
                }
            },
            'current_class': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control',
                    'id': 'current_class'
                }
            }
        }


class SearchClassForm(ModelForm):
    """
    SearchClass - Form for searching classes based on programme and admission year

    """
    class Meta:
        model = Class
        only = ['programme']
        field_args = {
            'programme': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control programme'
                }
            }
        }


# Forms for class records

class AddStaffForm(ModelForm):
    """
    AddStaff - Form for adding departments to staff

    """
    class Meta:
        model = Staff
        only = ['department']
        field_args = {
            'department': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control',
                    'placeholder': 'E.g. English or Geography'
                }
            }
        }


class SearchStaffForm(ModelForm):
    """
    SearchStaff - Form for searching staff based on department

    """
    class Meta:
        model = Staff
        
        department = QuerySelectField(
        'Department:',
        validators = [InputRequired()],
        query_factory=lambda: Staff.query.all(),
        render_kw={
            'class': "form-control dept"
        }
    )


# Forms for role records

class AddRoleForm(ModelForm):
    class Meta:
        model = Role
        only = ['purpose']
        field_args = {
            'purpose': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required':'',
                    'class': 'form-control account_type'
                }
            }
        }


# class SearchRoleForm(ModelForm):
#     class Meta:
#         model = Role
#         only = ['purpose']
#         field_args = {
#             'purpose': {
#                 'render_kw': {
#                     'autocomplete': 'off',
#                     'required':'',
#                     'class': 'form-control programme'
#                 }
#             }
#         }

        