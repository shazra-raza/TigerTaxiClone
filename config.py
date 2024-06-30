# ----------------------------------------------------------------------
# config.py
# Authors: Kwasi Oppong-Badu, Jude Muriithi
# Description: Defines object used to set app configuration variables in
# __init__.create_app()
# ----------------------------------------------------------------------

import os

# ----------------------------------------------------------------------

# Grabs config from environment variables (set with source .flaskenv)
class Config:
    # Sets secret key
    SECRET_KEY = os.environ.get("SECRET_KEY")

    # Sets server name (Heroku only)
    server = os.environ.get("SERVER_NAME")
    if server is not None:
        SERVER_NAME = server

    # Flask-SQLAlchemy setup (modified for Heroku)
    db_uri = os.environ.get("DATABASE_URL")

    if db_uri is None:
        pg_user = os.environ.get("POSTGRES_USER")
        pg_pass = os.environ.get("POSTGRES_PASSWORD")
        pg_host = os.environ.get("POSTGRES_HOST")
        pg_port = os.environ.get("POSTGRES_PORT")
        pg_db = os.environ.get("POSTGRES_DB")
        db_uri = "postgresql://{}:{}@{}:{}/{}".format(
            pg_user, pg_pass, pg_host, pg_port, pg_db
        )
    else:
        # Fix SQLAlchemy config url
        db_uri = db_uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = db_uri

    # Disables a feature of Flask-SQLAlchemy which sends a signal to
    # the app every time a change is about to be made in the database.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask-CAS-NG setup
    CAS_SERVER = os.environ.get("CAS_SERVER")
    CAS_AFTER_LOGIN = os.environ.get("CAS_AFTER_LOGIN")
    CAS_AFTER_LOGOUT = os.environ.get("CAS_AFTER_LOGOUT")

    # Flask-Mail setup
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = os.environ.get("MAIL_PORT")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")

    DEBUG = False
    TESTING = os.environ.get("FLASK_ENV") != "production"
    CSRF_ENABLED = True


# Subclasses for different deployment scenarios
class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    TESTING = True
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class TestingConfig(Config):
    TESTING = True
