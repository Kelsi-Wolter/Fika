'''Integration tests for Flask app'''

import server 
import unittest
from model import connect_to_db
from flask_sqlalchemy import SQLAlchemy


class FikaIntTest(unittest.TestCase):
    '''Unit tests for Fika App'''

    def setUp(self):
        '''Set up server for testing'''

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True
        server.app.secret_key = "kelsi's_project"

        # connect_to_db(app, 'postgresql:///testdb')
        # db = SQLAlchemy() 
        # db.create_all()
        # example_data()

    
    def test_index(self):
        '''Tests that homepage loads correctly'''

        result = self.client.get('/')
        self.assertIn(b'Explore Coffees', result.data)
        self.assertEqual(result.status_code, 200)

    def test_post(self):
        result = self.client.post('/login', data={'email': 'kelsi.wolter@gmail.com', 'password': '99'})
        self.assertIn(b'correct', result.data)


    def tearDown(self):
        pass

if __name__ == '__main__':
    unittest.main()