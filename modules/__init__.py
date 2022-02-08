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


@app.template_filter()
@pass_eval_context
def get_enum(eval_ctx, value):
    # Custom filter to return enumerated iterable
    return enumerate(value)


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
