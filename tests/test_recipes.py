import unittest
from app import  db
from models import Recipe,Ingredient
from base_test import BaseTestCase
class TestRecipes(BaseTestCase):


    def test_read_all_recipes(self):

        # create  tests recipes
        recipe1 = Recipe.query.filter_by(name="Cake").first()
        recipe2 = Recipe.query.filter_by(name="Pie").first()
        ingredient1 = Ingredient.query.filter_by(name="Flour").first()
        ingredient2 = Ingredient.query.filter_by(name="Sugar").first()



        # make a request to the endpoint API
        response = self.client.get('http://localhost:5000/api/recipes')
        # check the response status code
        self.assertEqual(response.status_code, 200)

        # check the response data
        expected_data = [
            {
                "id": recipe1.id,
                "name": "Cake",
                "ingredients": [
                    {"id": ingredient1.id, "name": "Flour"},
                    {"id": ingredient2.id, "name": "Sugar"}
                ],
                "cookTime": "1 hour",
                "serving": 8,
                "preparation": recipe1.preparation
            },
            {
                "id": recipe2.id,
                "name": "Pie",
                "ingredients": [
                    {"id": ingredient1.id, "name": "Flour"}
                ],
                "cookTime": "2 hours",
                "serving": 6,
                "preparation": recipe2.preparation
            }
        ]
        self.assertEqual(response.json, expected_data)
    
    # create a test recipe
    def test_create_new_recipe(self):

        data = {
                
                "name": "Muffins",
                "ingredients": [
                    {"name": "Flour"},
                    { "name": "Sugar"}
                ],
                "cookTime": "1 hour",
                "serving": 8,
                "preparation": "Mix ingredients"
            }
        
        # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/recipes', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 201)

        # check that the recipe was added to the database
        recipe = Recipe.query.filter_by(name="Muffins").first()
        self.assertIsNotNone(recipe)

        # check the response data
        ingredient1 = Ingredient.query.filter_by(name="Flour").first()
        ingredient2 = Ingredient.query.filter_by(name="Sugar").first()
        expected_data = {
                "id": recipe.id,
                "name": "Muffins",
                "ingredients": [
                    {'id': ingredient1.id, 'name': 'Flour'}, 
                    {'id': ingredient2.id, 'name': 'Sugar'}
                    ],
                "cookTime": "1 hour",
                "serving": 8,
                "preparation": "Mix ingredients"
            }
        self.assertEqual(response.json, expected_data)

    def test_create_existing_recipe(self):
        # create a test recipe
        data = {
                
                "name": "Cake",
                "ingredients": [
                    {"name": "Flour"},
                    { "name": "Sugar"}
                ],
                "cookTime": "1 hour",
                "serving": 8,
                "preparation": "Mix ingredients"
            }

        # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/recipes', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 406)

        # check that the recipe was not added to the database
        recipe = Recipe.query.filter_by(name="Cake").all()
        self.assertEqual(len(recipe), 1)

    def test_create_recipe_ingredient(self):
        # create a test recipe using an ingredient that does not exist.
        data = {
                
                "name": "Muffins",
                "ingredients": [
                    {"name": "milk"},
                    
                ],
                "cookTime": "1 hour",
                "serving": 8,
                "preparation": "Mix ingredients"
            }
        


        # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/recipes', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 404)

        
        self.assertEqual(response.json['detail'], "Ingredient milk not found, you should created first !")

    def test_filter_recipe(self):
        ingredient_name = "Sugar"
        # make a request to the endpoint API
        response = self.client.get(f'http://localhost:5000/api/recipes/{ingredient_name}')
        # check the response status code
        self.assertEqual(response.status_code, 200)



if __name__ == '__main__':
    unittest.main()