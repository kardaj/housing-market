# coding: utf8
import datetime
import pytz
from sqlalchemy import ForeignKeyConstraint, UniqueConstraint
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
LISTING_TYPES = ['house', 'apartment', 'land', 'parking']
AMENITY_TYPES = ['tram_stop', 'bus_stop', 'bike_stop']


def rollback_on_exception(f):
    def func_wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception:
            db.session.rollback()
            raise

    return func_wrapper


class GeometricType(object):
    geometry = db.Column(db.JSON, nullable=False)

    def get_center_coordinates(self):
        from shapely.geometry import shape
        my_poly = shape(self.geometry)
        return my_poly.interpolate(0.5, normalized=True).coords[0]


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password_hash = db.Column(db.String)


class Listing(db.Model, GeometricType):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    url = db.Column(db.String, unique=True, nullable=False)
    surface_area = db.Column(db.Float)
    room_count = db.Column(db.Integer)
    listing_type = db.Column(db.Enum(*LISTING_TYPES, name='listing_type'), nullable=False)
    is_furnished = db.Column(db.Boolean)
    attractiveness = db.Column(db.Float, default=0)


class Amenity(db.Model, GeometricType):
    __table_args__ = (
        UniqueConstraint('name', 'amenity_type', name='amenity_uix_1'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    amenity_type = db.Column(db.Enum(*AMENITY_TYPES, name='amenity_type'), nullable=False)
