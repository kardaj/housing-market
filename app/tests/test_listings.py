from app.tests import BaseTestCase


class TestListingResource(BaseTestCase):
    def test(self):
        r = self.client.listings()
        assert r.status_code == 200


class TestSearchListingResource(BaseTestCase):
    def test(self):
        r = self.client.search_listings(
            keywords='T2 hypercentre',
            min_surface_area=40,
            max_rent=700,
            amenities=['bike_stop'],
            listing_type='apartment'
        )
        print r.data
        assert r.status_code == 200
