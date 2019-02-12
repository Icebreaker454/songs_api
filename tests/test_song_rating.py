import pytest
import json


@pytest.fixture
def post(client):
    def post(url, data=None):
        return client.post(url, data=json.dumps(data), content_type='application/json')
    return post


class TestSongsRatingEndpoint:
    """ Tests for the songs rating endpoint - POST /songs/rating """

    def test_post_required(self, client):
        """ Test that POST requests are required """
        response = client.get('/songs/rating')
        assert response.status_code == 405

    def test_post_valid_data(self, post, mongo, sample_song):
        """ Valid POST request should create a song rating in MongoDB """
        assert mongo.db.song_ratings.count_documents({}) == 0
        payload = {
            'song_id': str(sample_song['_id']),
            'rating': 4
        }
        response = post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert f'Song {sample_song["_id"]} rated successfully' in response.json['data']['message']
        ratings = mongo.db.song_ratings.find({'song_id': str(sample_song['_id'])})
        assert ratings[0]['rating'] == 4

    def test_post_nonexistent_song(self, post, mongo, sample_song):
        """ Rating a nonexistent song should cause validation errors """
        assert mongo.db.song_ratings.count_documents({}) == 0
        payload = {
            'song_id': 'I should not exist',
            'rating': 5
        }
        response = post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert 'Invalid song id' in response.json['errors']['song_id']
        assert mongo.db.song_ratings.count_documents({}) == 0

    @pytest.mark.parametrize('rating,reason', [('A string', 'Not a valid integer.'),
                                               (6.7, 'Not a valid integer.'),
                                               (6, 'Rating should be between 1 and 5'),
                                               (0, 'Rating should be between 1 and 5')])
    def test_invalid_rating(self, post, mongo, sample_song, rating, reason):
        """ Invalid rating parameter should cause validation errors """
        assert mongo.db.song_ratings.count_documents({}) == 0
        payload = {
            'song_id': str(sample_song['_id']),
            'rating': rating
        }
        response = post('/songs/rating', data=payload)
        assert response.status_code == 200
        assert reason in response.json['errors']['rating']
        assert mongo.db.song_ratings.count_documents({}) == 0