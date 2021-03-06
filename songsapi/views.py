import bson

import flask
import marshmallow

from songsapi import app
from songsapi.extensions import mongo
from songsapi.schemas import SongRatingSchema


@app.route('/songs')
def songs_list():
    songs_cursor = mongo.db.songs.find()

    if 'offset' in flask.request.args:
        try:
            songs_cursor = songs_cursor.skip(int(flask.request.args['offset']))
        except (TypeError, ValueError):
            pass

    try:
        limit = int(flask.request.args.get('limit'))
    except (TypeError, ValueError):
        limit = app.config['PAGE_SIZE']
    songs_cursor = songs_cursor.limit(limit)

    return flask.jsonify({
        'data': [
            song for song in songs_cursor
        ]
    })


@app.route('/songs/avg/difficulty')
def average_difficulty():
    level = flask.request.args.get('level')
    try:
        params = {'level': {'$gte': int(level)}}
    except (TypeError, ValueError):
        params = {}

    result_cursor = mongo.db.songs.aggregate([
        {'$match': params},
        {
            '$group': {'_id': None, 'avg_difficulty': {'$avg': '$difficulty'}}
        }
    ])
    try:
        result = result_cursor.next()
        result = {'avg_difficulty': result['avg_difficulty']}
    except StopIteration:
        # We don't have results to aggregate on?
        result = None

    return flask.jsonify({
        'data': result
    })


@app.route('/songs/search')
def song_search():
    message = flask.request.args.get('message')
    return flask.jsonify({
        'data': [
            song for song in mongo.db.songs.find({'$text': {'$search': message}})
        ]
    })


@app.route('/songs/rating', methods=['POST'])
def song_rating():
    # Marshmallow `strict` schemas operate quite weirdly, so some kind of exception handling is necessary over here.
    try:
        rating_schema = SongRatingSchema(strict=True).load(flask.request.json)
        mongo.db.song_ratings.insert_one(rating_schema.data)
        return flask.jsonify({'data': {'message': f'Song {rating_schema.data["song_id"]} rated successfully'}})
    except marshmallow.exceptions.ValidationError as e:
        return flask.jsonify({'errors': e.args[0]})


@app.route('/songs/avg/rating/<song_id>')
def song_average_rating(song_id):
    try:
        cursor = mongo.db.song_ratings.aggregate([
            {'$match': {'song_id': bson.ObjectId(song_id)}},
            {
                '$group': {
                    '_id': None,
                    'avg_rating': {'$avg': '$rating'},
                    'min_rating': {'$min': '$rating'},
                    'max_rating': {'$max': '$rating'}
                }
            }
        ])
        result = cursor.next()
        result = {'min_rating': result['min_rating'],
                  'max_rating': result['max_rating'],
                  'avg_rating': result['avg_rating']}
    except (StopIteration, bson.errors.InvalidId):
        result = None

    return flask.jsonify({
        'data': result
    })
