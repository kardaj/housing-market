from flex.core import load, validate_api_call
from flex.exceptions import ValidationError
from app.conf import PROJECT_DIR
import os
import json


def strip_none(data):
    if isinstance(data, dict):
        return {k: strip_none(v) for k, v in data.items() if k is not None and v is not None}
    elif isinstance(data, list):
        return [strip_none(item) for item in data if item is not None]
    elif isinstance(data, tuple):
        return tuple(strip_none(item) for item in data if item is not None)
    elif isinstance(data, set):
        return {strip_none(item) for item in data if item is not None}
    else:
        return data


class Client(object):
    schema = load(os.path.join(PROJECT_DIR, 'app/swagger.yml'))

    def __init__(self, username, password, test_app=None, app=None):
        self.test_app = test_app
        self.username = username
        self.password = password
        self.app = app
        self.validate_api_call = True

    def put_user(self, user_id, username=None, email=None, notify=None):
        data = {'username': username, 'email': email, 'notify': notify}
        data = strip_none(data)
        return self.request('/users/{}'.format(user_id), method='PUT', data=data)

    def listings(self):
        return self.request('/listings')

    def search_listings(self,
                        keywords=None, min_rent=None, max_rent=None, min_room_count=None, max_room_count=None,
                        min_surface_area=None, max_surface_area=None, amenities=None, listing_type=None, limit=None):
        data = locals()
        data.pop('self')
        data = strip_none(data)
        return self.request('/listings:search', params=data)

    def amenity_types(self):
        return self.request('/amenity-types')

    def auth(self):
        return self.request('/auth')

    def request(self, url, method='GET', params=None, data=None, headers=None):
        import base64
        from urllib import urlencode
        import flask

        content_type = None
        if data is not None:
            data = json.dumps(data)
            content_type = 'application/json'
        if params is not None:
            params = {k: v for k, v in params.items() if v is not None}
            url = url + '?' + urlencode(params, True)
        if headers is None:
            headers = {}
        headers['Authorization'] = 'Basic ' + base64.b64encode(self.username + ':' + self.password)
        r = self.test_app.open(
            url,
            method=method, headers=headers, data=data, content_type=content_type)
        if self.validate_api_call:
            try:
                old_r_data = r.data
                r.data = json.dumps(strip_none(json.loads(r.data)))
            except ValueError:
                print(r.data)
            else:
                with self.app.test_request_context(url, method=method, headers=headers, data=data, content_type=content_type):
                    try:
                        validate_api_call(self.schema, raw_request=flask.request, raw_response=r)
                    except ValidationError as e:
                        context = {
                            'url': url,
                            'method': method,
                            'params': params,
                            'data': data,
                            'headers': headers,
                            'r.data': json.loads(r.data),
                        }
                        print(json.dumps(context, indent=4))
                        raise e
                r.data = old_r_data
        return r
