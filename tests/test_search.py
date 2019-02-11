import urllib.parse
import pytest

@pytest.fixture
def sample_songs_for_search(mongo):
    songs = [
        {"artist": "The Yousicians", "title": "The first song", "difficulty": 14.6, "level": 13,
         "released": "2016-10-26"},
        {"artist": "The Yousicians", "title": "Second song", "difficulty": 9.1, "level": 9, "released": "2010-02-03"},
        {"artist": "Mr Fastfinger", "title": "Third one", "difficulty": 15, "level": 13, "released": "2012-05-11"}]
    result = mongo.db.insert_many(songs)
    yield songs
    mongo.db.delete_many({'_id': {'$in': result.inserted_ids}})


class TestSongSearchEndpoint:
    """ Test case for the song search endpoint - GET /songs/search """

    def test_search_by_title_works(self, client, sample_songs_for_search):
        """ Search by song title should return relevant results """
        params = {'message': 'song'}
        response = client.get(f'/search?{urllib.parse.urlencode(params)}')
        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 2
        assert sample_songs_for_search[0] in data
        assert sample_songs_for_search[1] in data

    def test_search_by_author_works(self, client, sample_songs_for_search):
        """ Search by song author should return relevant results """
        params = {'message': 'Mr Fastfinger'}
        response = client.get(f'/search?{urllib.parse.urlencode(params)}')
        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 1
        assert sample_songs_for_search[2] in data

    def test_search_case_insensitive(self, client, sample_songs_for_search):
        """ Search should be case insensitive """
        params = {'message': 'the yousicians'}
        response = client.get(f'/search?{urllib.parse.urlencode(params)}')
        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 2
        assert sample_songs_for_search[0] in data
        assert sample_songs_for_search[1] in data
