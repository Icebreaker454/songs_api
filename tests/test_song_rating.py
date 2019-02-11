import pytest

@pytest.fixture
def sample_song(mongo):
    song = {'_id': '12345', 'title': 'Nah, just for testing purposes', 'album': 'DevOps dreams'}
    result = mongo.db.songs.insert_one(song)
    yield song
    mongo.db.songs.delete_one({'_id': result.inserted_id})


class TestSongsRatingEndpoint:
    """ Tests for the songs rating endpoint - POST /songs/rating """

    def test_post_required(self, client):
        """ Test that POST requests are required """
        response = client.get('/songs/rating')
        assert response.status_code == 405

    def test_post_valid_data(self, client, mongo, sample_song):
        """ Valid POST request should create a song rating in MongoDB """
        assert mongo.db.song_ratings.count() == 0
        payload = {
            'song_id': sample_song['_id'],
            'rating': 4
        }
        response = client.post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert f'Song {sample_song["_id"]} rated successfully' in response.json['data']['message']
        ratings = mongo.db.song_ratins.find({'song_id': sample_song['_id']})
        assert len(ratings) == 1
        assert ratings[0]['rating'] == 4

    def test_post_nonexistent_song(self, client, mongo):
        """ Rating a nonexistent song should cause validation errors """
        assert mongo.db.song_ratings.count() == 0
        payload = {
            'song_id': 'I should not exist',
            'rating': 5
        }
        response = client.post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert 'Invalid song id' in response.json['data']['errors']['song_id']
        assert mongo.db.song_ratings.count() == 0

    @pytest.mark.parametrize('rating,reason', [('Not a string', 'Rating should be an integer'),
                                               (6.7, 'Rating should be an integer'),
                                               (6, 'Rating should be between 1 and 5'),
                                               (0, 'Rating should be between 1 and 5')])
    def test_invalid_rating(self, client, mongo, sample_song, rating, reason):
        """ Invalid rating parameter should cause validation errors """
        assert mongo.db.song_ratings.count() == 0
        payload = {
            'song_id': sample_song['_id'],
            'rating': rating
        }
        response = client.post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert reason in response.json['data']['errors']['rating']
        assert mongo.db.song_ratings.count() == 0