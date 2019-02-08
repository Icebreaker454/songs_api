import flask

from songsapi import app
from songsapi.extensions import mongo


@app.route('/songs')
def index():
    return flask.jsonify({
        'data': [
            song for song in mongo.db.songs.find()
        ]
    })
