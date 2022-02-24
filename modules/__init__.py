"""
All initialisations like db = SQLAlchemy in this file
"""
import os
from zoneinfo import ZoneInfo

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect, FlaskForm
from flask_sqlalchemy import SQLAlchemy
from wtforms_alchemy import model_form_factory
from jinja2.filters import pass_eval_context
from pathlib import Path
from dotenv import load_dotenv


# Load .env file
# env_path = Path('.').parent.absolute() / 'env_vars/.env'

env_path = "/home/isolveit/Documents/myCodes/Codes/Work/libmgtsystem/project/env_vars/.env"
load_dotenv(dotenv_path=env_path)
app = Flask(__name__)

# app configs
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_SQLALCHEMY_DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('DEV_SECRET_KEY')

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)
csrf = CSRFProtect(app)
tzinfo, app_time_zone = ZoneInfo, ZoneInfo("UTC")

BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(cls):
        return db.session


# Custom jinja filters
@app.template_filter()
@pass_eval_context
def get_enum(eval_ctx, value):
    # Custom filter to return enumerated iterable
    return enumerate(value)


@app.template_filter()
@pass_eval_context
def get_track(eval_ctx, value):
    # Custom filter to get a shorthand version of student track
    # For example: if track value is GOLD, then the function will return GD
    text = value
    new_text = str(text.value)
    shorthand = f"{new_text[0]}{new_text[-1]}".upper()
    return shorthand


@app.template_filter()
@pass_eval_context
def get_course(eval_ctx, value):
    # Custom filter to get a shorthand version of student course
    # If the course value is one word, then the function will return the first 2 characters
    # or if the course value is two words, then the function will return the first character of each word
    # E.g.: BUSINESS = BU, GENERAL ARTS = GA
    text = value
    new_text = str(text.value).split(' ', 1)
    shorthand = f"{new_text[0][0]}{new_text[1][0]}".upper() if len(new_text) == 2 else f"{new_text[0][0]}{new_text[0][1]}".upper()
    return shorthand


@app.template_filter()
@pass_eval_context
def get_current_class(eval_ctx, value):
    # Custom filter to return the current class of a student
    from datetime import datetime as dt
    current_yr = dt.utcnow().year
    diff_year = current_yr - int(value)
    return diff_year


# Blueprints
from .users.view import users_bp
from .books.view import books_bp
from .tracking.view import tracking_bp
from .sysadmin.auth.view import auth_bp
from .sysadmin.dashboard.view import dashboard_bp
from .sysadmin.record_mgt.view import record_mgt_bp

# Register blueprints
app.register_blueprint(books_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(record_mgt_bp)
app.register_blueprint(tracking_bp)
