import os
from decouple import config
from flask_testing import TestCase

from config import TestConfig 
from app import app, db
from models import User,Ingredient, Recipe


class BaseTestCase(TestCase):
    def create_app(self):
        
            app.config.from_object(config("APP_SETTINGS")) 
        
            return app

    def setUp(self):
        with app.app_context():
           db.create_all()
           
           # Create user and admin for testing
           self.admin = User(name="adminTest", password="admin_password", is_admin=True)
           self.user = User(name="userTest", password="user_password")
           db.session.add(self.user)
           db.session.add(self.admin)
           db.session.commit()

           # create some test ingredients
           self.ingredient1 = Ingredient(name="Flour")
           self.ingredient2 = Ingredient(name="Sugar")
           db.session.add_all([self.ingredient1, self.ingredient2])
           db.session.commit()


           # create  tests recipes
           self.recipe1 = Recipe(name="Cake", cookTime="1 hour", serving=8, preparation="Mix ingredients")
           self.recipe2 = Recipe(name="Pie", cookTime="2 hours", serving=6, preparation="add ingredient1, bake")
           self.recipe1.ingredients = [self.ingredient1, self.ingredient2]
           self.recipe2.ingredients = [self.ingredient1]
           db.session.add_all([self.recipe1, self.recipe2])
           db.session.commit()



           

           with self.client.session_transaction() as sess:
            sess['name'] = self.admin.name
           

        

    def tearDown(self):
       with app.app_context():
          db.session.remove()
          db.drop_all()
          #testdb_path = os.path.join("welshAcademy_test.db")
          #os.remove(testdb_path)