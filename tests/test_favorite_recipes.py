import unittest
from app import  db
from flask import session
from models import User
from base_test import BaseTestCase
class TestFavoriteRecipes(BaseTestCase):
    
    def test_favorite_recipes(self):
        data = {
            "recipes":[
                {
                    "name": "Cake"
                },
                {
                    "name":"Pie"
                }
            ]
            
        }

         # make a request to the endpoint
        response = self.client.post('http://localhost:5000/api/favoriteRecipes', json=data)

        # check the response status code
        self.assertEqual(response.status_code, 201)
        with self.client.session_transaction() as sess:
           username = sess['name']

       
        current_User = User.query.filter_by(name=username).first()
         # check that the recipe was added to the database as favorite for the current user
        recipes = current_User.favoriteRecipes
        for recipe in recipes:
            self.assertIsNotNone(recipe)
            
        self.assertEqual(len(recipes), len(data["recipes"]))




        #Test delete a favorite recipe
        # make a request to the endpoint API
        response = self.client.delete('http://localhost:5000/api/favoriteRecipes', json=data)
        # check the response status code
        self.assertEqual(response.status_code, 201)
        
        recipes = current_User.favoriteRecipes
        self.assertEqual(len(recipes), 0)

        #Test list all favorite recipes
        # make a request to the endpoint API
        response = self.client.get('http://localhost:5000/api/favoriteRecipes')
        # check the response status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json,{'message': 'No favorite recipes found'})

       






if __name__ == '__main__':
    unittest.main()


