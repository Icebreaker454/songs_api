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
