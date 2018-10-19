from webargs import fields
from webargs.flaskparser import use_kwargs
from app import parse
from app.model import LISTING_TYPES, AMENITY_TYPES
from marshmallow import validate
from app.resources import DefaultSchema, DefaultResource
from app.model import db, Listing, rollback_on_exception
from webargs.flaskparser import use_kwargs


class ArgsListingSearch(DefaultSchema):
    keywords = fields.String(location='json')
    min_rent = fields.Integer(location='json')
    max_rent = fields.Integer(location='json')
    min_surface_area = fields.Integer(location='json')
    max_surface_area = fields.Integer(location='json')
    min_room_count = fields.Integer(location='json')
    max_room_count = fields.Integer(location='json')
    is_furnished = fields.Boolean(location='json', missing=False)
    listing_type = fields.String(
        required=True,
        location='query',
        validate=validate.OneOf(choices=LISTING_TYPES))
    amenities = fields.DelimitedList(fields.String(validate=validate.OneOf(
        choices=AMENITY_TYPES)), location='query', required=False)
    limit = fields.Integer(location='json', default=10)


class ListingResource(DefaultResource):
    @rollback_on_exception
    def get(self):
        listings = []
        longitudes = []
        latitudes = []
        bbox = []
        for listing in db.session.query(Listing).all():
            lng, lat = listing.get_center_coordinates()
            longitudes.append(lng)
            latitudes.append(lng)

            listings.append({
                'listing_id': listing.id,
                'name': listing.name,
                'surface_area': listing.surface_area,
                'attractiveness': listing.attractiveness,
                'roum_count': listing.room_cout,
                'listing_type': listing.listing_type,
                'latitude': lat,
                'longitude': lng
            })
        if longitudes and latitudes:
            bbox = [min(longitudes),  min(latitudes), max(longitudes), max(latitudes)]
        return self.jsonify({'listings': listings, 'bbox': bbox})


class ListingSearchResource(DefaultResource):
    @rollback_on_exception
    @use_kwargs(ArgsListingSearch)
    def get(self,
            keywords, min_rent, max_rent, min_surface_area, max_surface_area, min_room_count, max_room_count,
            is_furnished, listing_type, amenities, **kwargs):
        return []
