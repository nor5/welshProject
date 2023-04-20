import os
from decouple import config
from flask_testing import TestCase

from config import TestConfig 
from app import app, db
from models import User


class BaseTestCase(TestCase):
    def create_app(self):
        
            app.config.from_object(config("APP_SETTINGS")) 
        
            return app

    def setUp(self):
        with app.app_context():
           db.create_all()
        
           user = User(name="admin", password="admin_user")
           db.session.add(user)
           db.session.commit()
        

    def tearDown(self):
       with app.app_context():
          db.session.remove()
          db.drop_all()
          #testdb_path = os.path.join("welshAcademy_test.db")
          #os.remove(testdb_path)"""