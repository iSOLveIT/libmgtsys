from .models import Books
from project.modules import ModelForm

# from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired, Length, DataRequired
from wtforms.fields import SearchField


class AddBooksForm(ModelForm):
    """
    StudentForm - Form for adding students

    """

    class Meta:
        model = Books
        only = ['classification_no', 'title', 'author',
                'category', 'publication', 'qty_added',
                'catalogue_no', 'download_link']
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
            },
            'catalogue_no': {
                'render_kw': {
                    'autocomplete': 'off',
                    'class': 'form-control',
                    'maxlength': "30",
                    'minlength': "7",
                    'placeholder': 'e.g. SHELVE9_R10C3 (enter books location on shelve)'
                }
            },
            'download_link': {
                'render_kw': {
                    'autocomplete': 'off',
                    'type': 'url',
                    'class': 'form-control',
                    'placeholder': 'Paste Google Drive link to book file'
                }
            }
        }


class SearchBooksForm(ModelForm):
    """
    SearchBooksForm - Form for searching books

    """

    search_term = SearchField(u"Keyword", validators=[InputRequired(), DataRequired(), Length(min=4, max=30)],
                              render_kw={
                                  'autocomplete': 'off',
                                  'required': '',
                                  'class': 'form-control',
                                  'placeholder': 'Type Book Title or Author or Classification No. or Category',
                                  'hx-post': "/books/list",
                                  'hx-trigger': "keyup changed delay:500ms, search",
                                  'hx-target': "#results_box",
                                  'hx-swap': "outerHTML"
                              })
