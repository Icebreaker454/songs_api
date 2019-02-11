import flask
import marshmallow

from songsapi import app
from songsapi.extensions import mongo


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
