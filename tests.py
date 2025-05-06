import unittest
from app import app as flask_app
import json

class TestOfflinePOS(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()
        self.app.testing = True

    def test_login_success(self):
        response = self.app.post('/api/login', data=json.dumps({"username": "admin", "password": "password123"}), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["message"], "Login successful")

    def test_create_product(self):
        response = self.app.post('/api/products', data=json.dumps({
            "name": "Test Product",
            "price": 99.99,
            "stock": 10,
            "barcode": "789012"
        }), content_type='application/json')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["message"], "Product created successfully")

if __name__ == '__main__':
    unittest.main()
