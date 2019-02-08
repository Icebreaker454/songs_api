import songsapi
import pytest
from flask_pymongo import PyMongo

@pytest.fixture(scope='session')
def app():
    return songsapi.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def mongo(app):
    """ Instantiates a mongo client with test database access """
    client = PyMongo()
    client.init_app(app)
    client.db.command('dropDatabase')
    return client
