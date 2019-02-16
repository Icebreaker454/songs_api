# SongsAPI

This is a RESTful song API

## Quick Start

### Prerequisities

A working MongoDB instance located at `localhost:27017`

An easy way to setup using Docker:
```
$ docker pull mongo
$ docker run -p 27017:27017 mongo
```

### Clone the repository

```
$ git clone https://github.com/Icebreaker454/songs_api 
```

### Development
Install the dev extras package via setuptools
```
$ pip install -e '.[dev]'
```

Run the application
```
$ export SONGSAPI_SETTINGS=settings/default.py
$ export FLASK_APP=songsapi
$ flask run
```
It becomes available in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


### Popuate the database

```
$ flask import_songs var/songs.json
```


### Production
Install the application via setuptools
```
$ pip install -e .
```

Run the application
```
$ export SONGSAPI_SETTINGS=settings/default.py
$ export FLASK_APP=songsapi
$ FLASK_DEBUG=0 flask run
```



### Testing

The API includes tests written in PyTest.
It supports setuptools `test` command:
```
$ python setup.py test
```

As well as a regular pytest command:

```
$ pytest
```

