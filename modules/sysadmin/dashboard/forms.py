from datetime import datetime as dt, timedelta

from wtforms_alchemy import InputRequired, Length, DataRequired
from flask_wtf import FlaskForm
from wtforms.fields import DateField, StringField, IntegerField, SelectField


class BookTagForm(FlaskForm):
    """
    BookTagForm - Form for generating book tags
    """

    sch_name = StringField(
        "School's Name",
        validators=[InputRequired(), DataRequired(), Length(min=3, max=500)],
        render_kw={
            "class": "form-control",
            "placeholder": "e.g. SWEDRU SENIOR HIGH SCHOOL",
        },
    )
    book_title = StringField(
        "Book Title",
        validators=[InputRequired(), DataRequired(), Length(min=3, max=300)],
        render_kw={"class": "form-control", "placeholder": "e.g. I Told You So"},
    )
    classification_no = StringField(
        "Classification No.",
        validators=[InputRequired(), DataRequired(), Length(min=3, max=10)],
        render_kw={"class": "form-control", "placeholder": "e.g. LIT101"},
    )
    total_tags = IntegerField(
        "Number of Tags (less than 1000)",
        validators=[InputRequired(), DataRequired()],
        render_kw={
            "class": "form-control",
            "max": "1000",
            "min": "2",
            "step": "2",
            "placeholder": "Enter the number of tags to generate",
        },
    )
    tag_date = DateField(
        "Date",
        validators=[InputRequired(), DataRequired()],
        default=dt.utcnow(),
        render_kw={"class": "form-control"},
    )


class ReportForm(FlaskForm):
    """
    ReportForm - Form for generating reports
    """

    select_report = SelectField(
        "Report",
        choices=[
            ("", "Select Report"),
            ("users", "Users Report"),
            ("books", "Books Report"),
            ("books_issued", "Books Issued Report"),
        ],
        validators=[InputRequired(), DataRequired()],
        render_kw={
            "class": "form-control",
            "hx-get": "/dashboard/admin/reports",
            "hx-target": "#report_type",
        },
    )

    report_type = SelectField(
        "Report Type",
        choices=[("", "Select Report Type")],
        render_kw={"class": "form-control"},
    )

    start_date = DateField(
        "Start Date",
        validators=[InputRequired(), DataRequired()],
        default=dt.utcnow() - timedelta(days=30),
        render_kw={"class": "form-control", "max": dt.utcnow()},
    )

    end_date = DateField(
        "End Date",
        validators=[InputRequired(), DataRequired()],
        default=dt.utcnow(),
        render_kw={"class": "form-control", "max": dt.utcnow()},
    )
