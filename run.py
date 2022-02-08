import json

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from jinja2.filters import pass_eval_context
from pathlib import Path

from .config import app_config
from .init import db, migrate, login_manager
from .modules.books.view import books_bp
from .modules.users.view import users_bp
from .modules.tracking.view import tracking_bp
from .modules.sysadmin.auth.view import auth_bp
from .modules.sysadmin.dashboard.view import dashboard_bp
from .modules.sysadmin.record_mgt.view import record_mgt_bp


base_path = Path('.').parent.absolute()


def create_app(config_name):
    library_app = Flask(__name__, instance_relative_config=True)
    configuration = app_config[config_name]
    library_app.config.from_object(configuration)

    if config_name != "testing":
        # load the instance config, if it exists, when not testing
        library_app.config.from_pyfile("config.py", silent=True)

    # create empty instance folder and empty config if not present
    try:
        Path.mkdir(Path(library_app.instance_path))
        with open(Path.joinpath(Path(library_app.instance_path), "config.py"), "a"):
            pass
    except OSError:
        pass

    db.init_app(library_app)
    migrate.init_app(library_app, db)
    login_manager.init_app(library_app)
    csrf = CSRFProtect(library_app)

    # Register blueprints
    library_app.register_blueprint(books_bp)
    library_app.register_blueprint(users_bp)
    library_app.register_blueprint(auth_bp)
    library_app.register_blueprint(dashboard_bp)
    library_app.register_blueprint(record_mgt_bp)
    library_app.register_blueprint(tracking_bp)

    return library_app


# Read app environment from .json file
with open(Path.joinpath(base_path, "config.json")) as f:
    config_json = json.load(f)
environment = config_json["environment"]

app = create_app(environment)   # initialise app
# app.app_context().push()


@app.template_filter()
@pass_eval_context
def get_enum(eval_ctx, value):
    # Custom filter to return enumerated iterable
    return enumerate(value)


if __name__ == "__main__":
    app.run(port=4000)
