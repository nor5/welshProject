import os
import pathlib
from datetime import timedelta

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

basedir = pathlib.Path(__file__).parent.resolve()


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()


class Config:
    # provide additional security measures in a Flask application
    # protect against session-related attacks
    # used to encrypt and sign the session cookies,
    SECRET_KEY = os.environ["SECRET_KEY"]
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'welshAcademy_test.db'}"

    # track modifications of objects and emit signals if it is TRUE,
    # such as adding, modifying, or deleting records,
    SQLALCHEMY_TRACK_MODIFICATIONS = False
