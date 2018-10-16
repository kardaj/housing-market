from webargs import fields
from webargs.flaskparser import use_kwargs
from app import parse
from app.model import AMENITY_TYPES
from marshmallow import validate
from app.resources import DefaultResource


class AmenityTypesResource(DefaultResource):
    def get(self):
        return self.jsonify(AMENITY_TYPES)
