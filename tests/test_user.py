import unittest
from app import  db
from models import User
from base_test import BaseTestCase
class TestUserAccount(BaseTestCase):
    def test_create_user(self):
        #Create an admin for authentication 
        admin = User(name="adminTest", password="admin_user", is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
        # Login as the admin user
        with self.client.session_transaction() as sess:
            sess['name'] = 'adminTest'

        # Create a new user
        new_user = {
            "name": "test_user",
            "password": "test_password"
          }
        response = self.client.post('http://localhost:5000/api/UserRegistration', json=new_user)

        # Check the response status code and data
        self.assertEqual(response.status_code, 201)
        # Try to create a user with the same name
        response = self.client.post('http://localhost:5000/api/UserRegistration', json=new_user)

        # Check the response status code and data
        self.assertEqual(response.status_code, 409)
        self.assertEqual(response.json['detail'], "user test_user already exists")

        # Try to create a user without admin privileges
        with self.client.session_transaction() as sess:
           sess['name'] = 'test_user'
        response = self.client.post('http://localhost:5000/api/UserRegistration', json=new_user)

        # Check the response status code and data
        self.assertEqual(response.status_code, 406)
        self.assertEqual(response.json['detail'], "user test_user must be an admin to create a user")
    
    def test_login(self):
        #Create an admin for authentication 
        admin = User(name="adminTest", password="admin_user", is_admin=True)
        db.session.add(admin)
        db.session.commit()
        
        # Login as the admin user
        with self.client.session_transaction() as sess:
            sess['name'] = 'adminTest'

        # Create a new user
        new_user = {
            "name": "test_user",
            "password": "test_password"
          }
        response = self.client.post('http://localhost:5000/api/UserRegistration', json=new_user)

        # Check the response status code and data
        self.assertEqual(response.status_code, 201)
        response = self.client.post('http://localhost:5000/api/userLogin', json=new_user)
        # Check the response status code and data
        self.assertEqual(response.status_code, 201)
        
        # try to log in with the wrong password
        login_data = {
        "name": "test_user",
        "password": "wrong_password"
        }
        response = self.client.post('http://localhost:5000/api/userLogin', json=login_data)
        # Check the response status code and data
        self.assertEqual(response.status_code, 403)


if __name__ == '__main__':
    unittest.main()