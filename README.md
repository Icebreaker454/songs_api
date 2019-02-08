# SongsAPI

This is a RESTful song API

## Quick Start

### Prerequisities

A working MongoDB instance

### Development
Install the dev extras package via setuptools
```
pip install -e '.[dev]'
```

Run the application
```
export FLASK_APP=songsapi
flask run
```
And open it in the browser at [http://127.0.0.1:5000/](http://127.0.0.1:5000/)


### Production
Install the application via setuptools
```
pip install -e .
```

Run the application
```
export FLASK_APP=songsapi
FLASK_DEBUG=0 flask run
```