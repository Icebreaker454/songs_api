import flask
import marshmallow

from songsapi import app
from songsapi.extensions import mongo
from songsapi.schemas import PaginationSchema


@app.route('/songs')
def songs_list():
    pagination = PaginationSchema().load(flask.request.args)
    songs_cursor = mongo.db.songs.find()
    if 'offset' in pagination.data:
        songs_cursor = songs_cursor.skip(pagination.data['offset'])
    songs_cursor = songs_cursor.limit(pagination.data.get('limit') or app.config['PAGE_SIZE'])

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
