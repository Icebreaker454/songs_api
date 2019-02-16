import os
from flask import Flask

from songsapi.extensions import mongo
from songsapi.json_encoder import MongoIdJsonEncoder

app = Flask(__name__)
app.config.from_object('songsapi.settings')
app.config.from_envvar('SONGSAPI_SETTINGS')

# For painless serialization of mongo ObjectIDs
app.json_encoder = MongoIdJsonEncoder

mongo.init_app(app)

if os.environ.get('FLASK_DEBUG', True):
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'songsapi.log'), 'midnight')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

import songsapi.views  # noqa
import songsapi.commands  # noqa
