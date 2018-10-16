from webargs import fields
from webargs.flaskparser import use_kwargs
from app import parse
from app.model import LISTING_TYPES
from marshmallow import validate
from app.resources import DefaultSchema, DefaultResource
from app.model import db, Listing, rollback_on_exception
from webargs.flaskparser import use_kwargs


class ArgsListingSearch(DefaultSchema):
    name = fields.String(required=True, location='json')
    listing_url = fields.String(required=True, location='json', validate=validate.URL)
    size_in_meters = fields.Float(required=True, location='json')
    room_count = fields.Integer(required=True, location='json')
    is_furnished = fields.Boolean(location='json', missing=False)
    accomodation_type = fields.String(
        required=True,
        location='query',
        validate=validate.OneOf(choices=LISTING_TYPES))
    geometry = fields.Dict(
        required=True,
        location='json',
        validate=parse.validate_geometry)


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
            keywords, min_surface_area, max_surface_area, min_room_count, max_room_count, is_furnished,
            accomodation_type, listing_type, amenities, **kwargs):
        return []
