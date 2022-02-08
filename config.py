import os
from pathlib import Path
from dotenv import load_dotenv

base_path = Path('.').parent.absolute()


class BaseConfig:
    """Parent configuration class."""

    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BASE_DIR = base_path


class ProductionConfig(BaseConfig):
    """Configurations for production"""

    # Load .env file
    env_path = Path('.').parent.absolute() / 'env_vars/.env'
    load_dotenv(dotenv_path=env_path)

    # built in flask configs
    ENV = "production"
    SECRET_KEY = os.environ.get("PROD_SECRET_KEY")

    # database configs
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get(
            "PROD_SQLALCHEMY_DATABASE_URI",
            default="postgresql+psycopg2://isolveit:pswd#1234@localhost:8432/lib_dev"
        )
    )

    # unknown configs
    PASSWORD_SALT = os.environ.get("PROD_PASSWORD_SALT")


class DevelopmentConfig(BaseConfig):
    """Configurations for development"""

    # built in flask configs
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "secretisasecretandnothingbutasecret"

    # database configs
    # Add the below line with corrected values in config.py
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://isolveit:pswd#1234@localhost:8432/lib_dev'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://randy:Password#1234@localhost/lib_dev'

    # unknown configs
    PASSWORD_SALT = "is not salt for food but a password salt"


app_config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
}
