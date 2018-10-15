from webargs import fields
from webargs.flaskparser import use_kwargs
from app import parse
from model import AMENITY_TYPES
from marshmallow import validate
from app.resources import DefaultSchema


class ArgsAmenity(DefaultSchema):
    name = fields.String(required=True, location='json')
    amenity_type = fields.String(required=True, location='query', validate=validate.OneOf(choices=AMENITY_TYPES))
    geometry = fields.Dict(required=True, location='json', validate=parse.validate_geometry)
