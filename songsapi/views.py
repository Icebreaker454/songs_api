import flask

from songsapi import app
from songsapi.extensions import mongo


def prepare_song(song):
    song['id'] = str(song.pop('_id'))
    return song


@app.route('/songs')
def index():
    return flask.jsonify({
        'data': [
            prepare_song(song) for song in mongo.db.songs.find()
        ]
    })
