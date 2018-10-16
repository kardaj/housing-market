from app.authentication import auth
from marshmallow import Schema
from flask_restful import Resource
from flask import Response
from flask import make_response
import json
import datetime


class DefaultSchema(Schema):
    class Meta:
        strict = True


def serialize(data):
    if isinstance(data, list):
        data = [serialize(x) for x in data]
    elif isinstance(data, dict):
        for k, v in data.items():
            data[k] = serialize(v)
    elif isinstance(data, datetime.datetime):
        if data.tzinfo is None:
            data = data.replace(tzinfo=pytz.utc)
        data = data.isoformat()
    elif isinstance(data, unicode):
        data = data.encode('UTF-8')
    # TODO add the case below to qrestAPI's basic `serialize` function!
    elif isinstance(data, datetime.date):
        data = data.isoformat()
    return data


class DefaultResource(Resource):
    method_decorators = [auth.login_required]

    def jsonify(self, data, status_code=200, additional_headers=None):
        if isinstance(data, Response):
            r = data
            if 'application/json' not in r.mimetype.lower():
                raise ValueError('Not JSON MimeType')
        else:
            if data not in [{}, None]:
                serialized_data = serialize(data)
            else:
                serialized_data = data
            json_data = json.dumps(serialized_data, ensure_ascii=False)
            r = make_response(json_data, status_code)
            if additional_headers is not None:
                for name, value in additional_headers.iteritems():
                    # this is not a dict, can't use `dict.update`
                    r.headers[name] = value
            r.mimetype = 'application/json; charset=utf-8'
        return r
