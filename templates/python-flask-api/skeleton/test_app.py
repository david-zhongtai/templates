import unittest
from app import app

class FlaskAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        """Test health check endpoint"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['status'], 'healthy')

    def test_get_items(self):
        """Test getting all items"""
        response = self.app.get('/api/v1/items')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('items', data)
        self.assertIn('count', data)

    def test_create_item(self):
        """Test creating a new item"""
        new_item = {
            "name": "Test Item",
            "description": "Test Description"
        }
        response = self.app.post('/api/v1/items',
                                json=new_item,
                                content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'Test Item')

    def test_get_item_by_id(self):
        """Test getting a specific item"""
        response = self.app.get('/api/v1/items/1')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)
        self.assertEqual(data['id'], 1)

    def test_get_nonexistent_item(self):
        """Test getting a non-existent item"""
        response = self.app.get('/api/v1/items/999')
        self.assertEqual(response.status_code, 404)

    def test_update_item(self):
        """Test updating an item"""
        updated_data = {
            "name": "Updated Item",
            "description": "Updated Description"
        }
        response = self.app.put('/api/v1/items/1',
                               json=updated_data,
                               content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Updated Item')

    def test_delete_item(self):
        """Test deleting an item"""
        response = self.app.delete('/api/v1/items/2')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

