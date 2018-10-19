from app.tests import BaseTestCase


class TestAmenityTypesResource(BaseTestCase):
    def test_amenity_types(self):
        r = self.client.amenity_types()
        assert r.status_code == 200
