import bson

from marshmallow import Schema, fields, ValidationError

from songsapi.extensions import mongo


class StrictInteger(fields.Integer):
    """" Override fields.Number string to num coercion """
    def _format_num(self, value):
        """ Check instance of int  or raise a :exc:`ValidationError` if an error occurs."""
        if value is None:
            return None
        if not isinstance(value, self.num_type):
            raise ValidationError("Not a valid integer.")
        return value


def check_song_exists(value):
    try:
        assert mongo.db.songs.count_documents({'_id': bson.ObjectId(value)})
    except (AssertionError, bson.errors.InvalidId):
        raise ValidationError('Invalid song id')


def check_rating(value):
    if value > 5 or value < 1:
        raise ValidationError('Rating should be between 1 and 5')
    return True


class SongRatingSchema(Schema):
    song_id = fields.String(validate=check_song_exists)
    rating = StrictInteger(validate=check_rating)