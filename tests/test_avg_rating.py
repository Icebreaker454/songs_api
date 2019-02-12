import pytest


@pytest.fixture
def song_ratings(sample_song, song_rating_factory, mongo):
    ratings = [song_rating_factory(sample_song['_id']) for _ in range(100)]
    result = mongo.db.song_ratings.insert_many(ratings)
    for rating in ratings:
        rating['_id'] = str(rating['_id'])
    yield ratings
    mongo.db.song_ratings.delete_many({'_id': {'$in': result.inserted_ids}})


class TestAverageSongRating:
    """ Test suite for average song rating endpoint - GET /songs/avg/rating/<song_id> """

    def test_averages_calculated_correctly(self, client, sample_song, song_ratings):
        """ Test that aggregation parameters for the song are calculated correctly """
        response = client.get(f'/songs/avg/rating/{sample_song["_id"]}')
        assert response.status_code == 200
        ratings = [r['rating'] for r in song_ratings]
        avg_rating = response.json['data']['avg_rating']
        assert avg_rating == sum(ratings) / len(ratings)
        min_rating = response.json['data']['min_rating']
        assert min_rating == min(ratings)
        max_rating = response.json['data']['max_rating']
        assert max_rating == max(ratings)

    def test_empty_if_invalid_song_id(self, client, sample_song, song_ratings):
        """ Aggregation params for nonexistent songs should be null """
        response = client.get(f'/songs/avg/rating/Not_a_valid_song_id')
        assert response.status_code == 200
        assert not response.json['data']
