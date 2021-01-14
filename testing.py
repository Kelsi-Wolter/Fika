'''Integration tests for Flask app'''

import server 
import unittest

class FikaIntTest(unittest.TestCase):
    '''Unit tests for Fika App'''

    def setUp(self):
        '''Set up server for testing'''

        self.client = server.app.test_client()
        server.app.config['TESTING'] = True

    
    def test_index(self):
        client = server.app.test_client()
        result = client.get('/')
        self.assertIn(b'Explore Coffees', result.data)

if __name__ == '__main__':
    unittest.main()