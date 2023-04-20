import unittest
from app import app, db
from base_test import BaseTestCase
class TestAppRoute(BaseTestCase):
    def test_home_redirect(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, '/api/ui/')
        
    
    

if __name__ == '__main__':
    unittest.main()