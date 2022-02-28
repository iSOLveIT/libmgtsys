# from datetime import datetime as dt

from project.modules.users.models import User
from project.modules import ModelForm

# from wtforms_alchemy.fields import QuerySelectField
# from wtforms_alchemy import InputRequired


class LoginForm(ModelForm):
    class Meta:
        model = User
        only = ['id', 'password']
        field_args = {
            'id': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'Student ID or Staff ID or Admin ID'
                }
            },
            'password': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': ''
                }
            }
        }


class RegistrationForm(ModelForm):
    class Meta:
        model = User
#
# class TalkActivityForm(ModelForm):
#     class Meta:
#         model = Activity
#         exclude = ['talk_id', 'type', 'text', 'note']
#
#         field_args = {
#             'start_time': {
#                 'render_kw': {
#                     'autocomplete': 'off',
#                     'required': ''
#                 }
#             },
#             'end_time': {
#                 'render_kw': {
#                     'autocomplete': 'off',
#                     'required': ''
#                 }
#             }
#         }
#
#     talks = QuerySelectField(
#         'Talk:',
#         validators=[InputRequired()],
#         query_factory=lambda: Talk.query.filter(
#             Talk.year == dt.utcnow().year,
#             Talk.accepted == 'accepted'
#         ).all(),
#         render_kw={
#             'class': "max-w-md"
#         }
#     )
