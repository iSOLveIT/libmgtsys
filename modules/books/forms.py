from .models import Books, Book
from project.modules import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired, Length, DataRequired
from wtforms.fields import StringField, URLField


class AddBooksForm(ModelForm):
    """
    StudentForm - Form for adding students

    """

    class Meta:
        model = Books
        only = ['classification_no', 'title', 'author',
                'category', 'publication', 'qty_added']
        field_args = {

            'classification_no': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'e.g. ENG203'
                }
            },
            'title': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'e.g. The White Whale'
                }
            },
            'author': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'e.g. Elon Musk'
                }
            },
            'category': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'id': 'c-category'
                }
            },
            'publication': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'e.g. PM Printing Press'
                }
            },
            'qty_added': {
                'render_kw': {
                    'autocomplete': 'off',
                    'required': '',
                    'class': 'form-control',
                    'placeholder': 'Enter number of books added'
                }
            }
        }
