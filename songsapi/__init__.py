import os
from flask import Flask

from songsapi.extensions import mongo

app = Flask(__name__)
app.config.from_object('songsapi.default_settings')
mongo.init_app(app)

if not app.debug:
    import logging
    from logging.handlers import TimedRotatingFileHandler
    # https://docs.python.org/3.6/library/logging.handlers.html#timedrotatingfilehandler
    file_handler = TimedRotatingFileHandler(os.path.join(app.config['LOG_DIR'], 'songsapi.log'), 'midnight')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('<%(asctime)s> <%(levelname)s> %(message)s'))
    app.logger.addHandler(file_handler)

import songsapi.views  # noqa
import songsapi.commands  # noqa
