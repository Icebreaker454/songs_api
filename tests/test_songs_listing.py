import urllib.parse


class TestSongsListing:
    """ Test suite for songs api listing page  - GET /songs """

    def test_songs_displayed(self, client, sample_songs):
        """ All songs stored in DB should be returned in the response """
        response = client.get('/songs')
        assert response.status_code == 200
        data = response.json['data']
        assert data == sample_songs

    def test_default_pagination(self, app, client, sample_songs):
        """ Test that default pagination is applied """
        response = client.get('/songs')
        data = response.json['data']
        assert len(data) == app.config['PAGE_SIZE']

    def test_pagination_works(self, client, sample_songs):
        """ Custom pagination arguments - limit and offset should work """
        params = {
            'limit': 5, 'offset': 3
        }
        response = client.get(f'/songs?{urllib.parse.urlencode(params)}')
        assert response.status_code == 200
        data = response.json['data']
        assert len(data) == 5
        assert data == sample_songs[3:8]

    def test_pagination_invalid_arguments(self, app, client, sample_songs):
        """ Invalid pagination data should be ignored"""
        params = {
            'limit': 'invalid limit', 'offset': 'invalid offset'
        }
        response = client.get(f'/songs?{urllib.parse.urlencode(params)}')
        data = response.json['data']
        assert response.status_code == 200
        assert len(data) == app.config['PAGE_SIZE']
        assert data == sample_songs[:app.config['PAGE_SIZE']]
