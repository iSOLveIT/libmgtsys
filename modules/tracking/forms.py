from datetime import datetime as dt

from project.modules.users.models import User
from project.modules import ModelForm

from wtforms_alchemy.fields import QuerySelectField
from wtforms_alchemy import InputRequired, Length
from wtforms.fields import DateField, SearchField
from flask_wtf import FlaskForm


class SearchBooksForm(ModelForm):
    """
    SearchBooksForm - Form for searching books

    """

    search_term = SearchField(u"Keyword", validators=[InputRequired(), Length(min=4, max=30)],
                              render_kw={
                                  'autocomplete': 'off',
                                  'required': '',
                                  'class': 'form-control',
                                  'placeholder': 'Type Book Title or Author or Classification No. or Category',
                                  'hx-post': "/tracking/get_books",
                                  'hx-trigger': "keyup changed delay:500ms, search",
                                  'hx-target': "#results_box",
                                  'hx-swap': "outerHTML"
                              })


class IssueBookForm(FlaskForm):
    """
    IssueBookForm - Forms for issuing book to user

    """

    borrowed_by = QuerySelectField(
        'Borrowed By:',
        validators=[InputRequired()],
        query_factory=lambda: User.query.order_by(User.role_id == 1,
                                                  User.role_id == 2).all(),
        get_label=User.label_for_user_sid,
        render_kw={'style': "height: calc(2.25rem + 2px);"}
    )

    return_date = DateField(u"Return Date", validators=[InputRequired()], default=dt.utcnow(),
                            render_kw={'style': "height: calc(2.25rem + 2px);",
                                       'min': dt.utcnow()})

    def validate_return_date(self):
        return False if self.return_date.data < dt.utcnow() else True
