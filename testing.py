'''Integration tests for Flask app'''

import server 
import unittest
import os
from model import connect_to_db, db, example_data
from flask_sqlalchemy import SQLAlchemy

os.system('dropdb FikaTest')
os.system('createdb FikaTest')

class FikaIntTestDB(unittest.TestCase):
    '''Unit tests for Fika App using fake database'''

    def setUp(self):
        '''Set up server for testing'''

        # Set up test client
        server.app.config['TESTING'] = True
        server.app.secret_key = "kelsi's_project"
        self.client = server.app.test_client()

        # Create example database to use for tests
        connect_to_db(server.app, 'postgresql:///FikaTest')
        db.create_all()
        example_data()

        # Put user in session
        with self.client as c:
            with c.session_transaction() as sess:
                sess['user'] = 1
                logged_in = sess['user']

    
    def test_index(self):
        '''Tests that homepage loads correctly'''

        result = self.client.get('/')
        self.assertIn(b'Explore Coffees', result.data)
        self.assertEqual(result.status_code, 200)

    def test_directory(self):
        '''Tests that roaster directory page will load with fake roaster'''

        result = self.client.get('/roaster_directory')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'City Girl', result.data)
        self.assertIn(b"Minnesota's Small Batch Coffee Roasters", result.data)

    def test_fake_roaster_details(self):
        '''Tests that details page will populate from fake DB'''

        result = self.client.get('/roaster_directory/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'City Girl', result.data)
        self.assertIn(b'Average User Rating: 3.5', result.data)


    # def test_post(self):
    #     # result = self.client.post('/login', data={'email': 'kelsi.wolter@gmail.com', 'password': '99'})
    #     # self.assertIn(b'correct', result.data)
    #     # does not work because password field does not show up in server response

    #     pass

    def test_user_page(self):
        '''Tests that user page loads with user in session from set up'''

        result = self.client.get('/account/1')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Welcome Admin', result.data)


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        db.engine.dispose()

if __name__ == '__main__':
    unittest.main()