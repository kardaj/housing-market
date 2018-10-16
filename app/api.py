from flask import Flask
import flask_restful
from flask_cors import CORS
from app.model import db
from app.resources.user import UserResource, AuthResource
from app.resources.listing import ListingResource, ListingSearchResource
from app.resources.amenity import AmenityTypesResource
from app import app_conf


app = Flask(__name__)

app.config.from_object(app_conf)
api = flask_restful.Api(app)
CORS(app,
     allow_headers=['authorization', 'content-type', 'if-modified-since'],
     expose_headers=['last-modified'])
db.init_app(app)


api.add_resource(AuthResource, '/auth')
api.add_resource(UserResource, '/users/<user_id>')
api.add_resource(ListingResource, '/listings')
api.add_resource(ListingSearchResource, '/listings:search')
api.add_resource(AmenityTypesResource, '/amenity-types')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=9999, debug=False)
