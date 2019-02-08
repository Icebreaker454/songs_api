import pytest


@pytest.fixture
def sample_songs(mongo):
    songs = [
        {'artist': 'The Yousicians', 'title': 'Lycanthropic Metamorphosis', 'difficulty': 14.6, 'level': 13,
         'released': '2016-10-26'},
        {'artist': 'The Yousicians', 'title': 'A New Kennel', 'difficulty': 9.1, 'level': 9, 'released': '2010-02-03'},
        {'artist': 'Mr Fastfinger', 'title': 'Awaki-Waki', 'difficulty': 15, 'level': 13, 'released': '2012-05-11'},
        {'artist': 'The Yousicians', 'title': "You've Got The Power", 'difficulty': 13.22, 'level': 13,
         'released': '2014-12-20'}
    ]
    result = mongo.db.songs.insert_many(songs)
    for song in songs:
        song['_id'] = str(song['_id'])
    yield songs
    # Cleanup
    mongo.db.songs.delete_many({'id': {'$in': result.inserted_ids}})


class TestSongsListing:
    """ Test suite for songs api listing page  - GET /songs """

    def test_songs_displayed(self, client, sample_songs):
        """ All songs stored in DB should be returned in the response """
        response = client.get('/songs')
        data = response.json['data']
        assert data == sample_songs
