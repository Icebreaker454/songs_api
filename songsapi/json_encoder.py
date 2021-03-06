import flask
import bson


class MongoIdJsonEncoder(flask.json.JSONEncoder):
    def default(self, o):
        if isinstance(o, bson.ObjectId):
            return str(o)
        return super().default(o)
