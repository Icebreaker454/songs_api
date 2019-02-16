import random
import string

# Sometimes, the average difficulty calculated has a calculation error of about 1e-10 due to Python's floating point
# calculation inaccuracy. Thus, I seeded the random module for tests reproducibility.
# http://effbot.org/pyfaq/why-are-floating-point-calculations-so-inaccurate.htm
random.seed(1337)

import pytest
from flask_pymongo import PyMongo

import songsapi


@pytest.fixture(scope='session')
def app():
    app = songsapi.app
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture(scope='session')
def mongo(app):
    ''' Instantiates a mongo client with test database access '''
    client = PyMongo()
    client.init_app(app)
    client.db.command('dropDatabase')
    return client


@pytest.fixture
def song_factory():
    def factory(artist=None, title=None, difficulty=None, level=None):
        return {
            'artist': artist or random.choice(['Elvis Presley', 'A Day to Remember', 'Metallica', 'Black Sabbath']),
            'title': title or ''.join(random.choices(string.ascii_uppercase + string.digits, k=32)),
            'difficulty': difficulty or random.uniform(5, 15),
            'level': level or random.randint(1, 15),
            'released': '1978-12-01'
        }
    return factory


@pytest.fixture
def song_rating_factory():
    def factory(song_id, rating=None):
        return {
            'song_id': song_id,
            'rating': rating or random.randint(1, 5)
        }
    return factory


@pytest.fixture
def sample_songs(mongo, song_factory):
    songs = [song_factory() for _ in range(20)]
    result = mongo.db.songs.insert_many(songs)
    for song in songs:
        song['_id'] = str(song['_id'])
    yield songs
    # Cleanup
    mongo.db.songs.delete_many({'_id': {'$in': result.inserted_ids}})


@pytest.fixture
def sample_song(mongo):
    mongo.db.song_ratings.delete_many({})
    song = {'title': 'Nah, just for testing purposes', 'album': 'DevOps dreams'}
    result = mongo.db.songs.insert_one(song)
    yield song
    mongo.db.songs.delete_one({'_id': result.inserted_id})
