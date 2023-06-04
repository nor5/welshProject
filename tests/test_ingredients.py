import unittest
from app import  db
from models import Ingredient
from base_test import BaseTestCase
class TestIngredients(BaseTestCase):

    def test_read_all_ingredients(self):


        # make a request to the endpoint API
        response = self.client.get('http://localhost:5000/api/ingredients')
        # check the response status code
        self.assertEqual(response.status_code, 200)
         
        # check the response data
        ingredient1 = Ingredient.query.filter_by(name="Flour").first()
        ingredient2 = Ingredient.query.filter_by(name="Sugar").first()
        expected_data = [
            {"id": ingredient1.id, "name": "Flour"},
            {"id": ingredient2.id, "name": "Sugar"}
        ]
        self.assertEqual(response.json, expected_data)
    
    
    def test_create_new_ingredient(self):
        # create a test ingredient
        data = {"name": "milk"}
        
        # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/ingredients', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 201)

        # check that the ingredient was added to the database
        ingredient = Ingredient.query.filter_by(name="milk").first()
        self.assertIsNotNone(ingredient)

        # check the response data
        expected_data = {"id": ingredient.id, "name": "milk"}
        self.assertEqual(response.json, expected_data)

    def test_create_existing_ingredient(self):
        # create a test ingredient
        data = {"name": "Sugar"}
       

        # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/ingredients', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 406)

        # check that the ingredient was not added to the database
        ingredients = Ingredient.query.filter_by(name="Sugar").all()
        self.assertEqual(len(ingredients), 1)

    


if __name__ == '__main__':
    unittest.main()
