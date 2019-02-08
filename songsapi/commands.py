import json

import click

from songsapi import app
from songsapi.extensions import mongo


class ImportException(Exception):
    def __init__(self, obj, errors):
        self.obj = obj
        self.errors = errors

    def __str__(self):
        return f'Got the following errors while importing {self.obj}: \n {self.errors}'


@app.cli.command('import_songs')
@click.argument('filename', type=click.File())
def import_songs(input_file):
    """
    Uploads data from sample file into application Storage
    :param input_file: the file descriptor read songs from
    :return: None
    """
    count = 0
    for line in input_file.readlines():
        song = json.loads(line)
        mongo.db.songs.insert_one(song)
        # A bit ugly, but efficient
        count += 1
    app.logger.info(f'DONE: Inserted: {count} records')
