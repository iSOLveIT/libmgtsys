from datetime import datetime as dt

from wtforms_alchemy import InputRequired, Length, DataRequired
from flask_wtf import FlaskForm
from wtforms.fields import DateField, StringField, IntegerField


class BookTagForm(FlaskForm):
    """
    BookTagForm - Form for generating book tags
    """

    book_title = StringField(u"Book Title", validators=[InputRequired(), DataRequired(), Length(min=10, max=300)],
                             render_kw={'class': "form-control", 'placeholder': "e.g. I Told You So"})
    classification_no = StringField(u"Classification No.",
                                    validators=[InputRequired(), DataRequired(), Length(min=3, max=10)],
                                    render_kw={'class': "form-control", 'placeholder': "e.g. LIT101"})
    total_tags = IntegerField(u"Number of Tags", validators=[InputRequired(), DataRequired(), Length(min=2, max=1000)],
                              render_kw={'class': "form-control",
                                         'placeholder': "Enter the number of tags to generate"})
    tag_date = DateField(u"Date", validators=[InputRequired(), DataRequired()], default=dt.utcnow(),
                         render_kw={'class': "form-control"})
