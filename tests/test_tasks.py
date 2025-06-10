
import unittest
import json
from app import create_app
from config.database import db_instance

class TaskAPITestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Clean up test data
        db_instance.get_collection('tasks').delete_many({})
    
    def tearDown(self):
        # Clean up test data
        db_instance.get_collection('tasks').delete_many({})
        self.app_context.pop()
    
    def test_create_task(self):
        task_data = {
            'title': 'Test Task',
            'description': 'This is a test task',
            'priority': 'high'
        }
        
        response = self.client.post('/api/tasks',
                                  data=json.dumps(task_data),
                                  content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertEqual(data['data']['title'], 'Test Task')
    
    def test_get_tasks(self):
        response = self.client.get('/api/tasks')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIsInstance(data['data'], list)
    
    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'healthy')

if __name__ == '__main__':
    unittest.main()