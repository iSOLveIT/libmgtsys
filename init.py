"""
All initialisations like db = SQLAlchemy in this file
"""

try:
    from zoneinfo import ZoneInfo
except ImportError:
    from backports.zoneinfo import ZoneInfo

from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms_alchemy import model_form_factory


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
tzinfo, app_time_zone = ZoneInfo, ZoneInfo("UTC")

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session
