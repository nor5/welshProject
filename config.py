import pathlib

from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_migrate import Migrate
from flask import Flask

basedir = pathlib.Path(__file__).parent.resolve()


db = SQLAlchemy()
ma = Marshmallow()
bcrypt = Bcrypt()
migrate = Migrate()
class Config:
    SECRET_KEY = 'welshAcademyTest'
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=10)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'welshAcademy.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / 'welshAcademy_test.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
