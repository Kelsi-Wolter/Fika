'''Following tutorial from Flask website'''

import os
import tempfile
import server
import pytest




@pytest.fixture
def client():
    db_test, server.app.config['DATABASE'] = tempfile.mkstemp()
    server.app.config['TESTING'] = True

    with server.app.test_client() as client:
        with server.app.app_context():
            server.connect_to_db(server.app)
        yield client

    os.close(db_test)
    os.unlink(server.app.config['DATABASE'])


def test_empty_db(client):
    '''Starts at homepage with no user in session'''

    rv = client.get('/')
    assert b'Create An Account' in rv.data 
