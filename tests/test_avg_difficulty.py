class TestAverageDifficulty:
    """ Test suite for the GET /songs/avg/difficulty endpoint """

    def test_average_calculated_correctly(self, client, sample_songs):
        """ Average should be calculated correctly """
        response = client.get('/songs/avg/difficulty')
        assert response.status_code == 200
        assert response.json['data']['avg_difficulty'] == sum(
            [s['difficulty'] for s in sample_songs]) / len(sample_songs)

    def test_level_argument_works(self, client, sample_songs):
        """ Level parameter should filter songs starting from a certain level """
        pass