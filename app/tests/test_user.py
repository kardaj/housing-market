from app.tests import BaseTestCase
from app.resources.user import create_user
import json


class TestUserResource(BaseTestCase):
    def test_auth(self):
        self.username = 'toto'
        self.password = 'toto12'
        email = 'toto@yahoo.fr'
        create_user(self.username, self.password, email=email)
        r = self.client.auth()
        assert r.status_code == 200
        user_dict = json.loads(r.data)
        r = self.client.put_user(user_dict['user_id'], email='notanemail')
        assert r.status_code == 422
        r = self.client.put_user(user_dict['user_id'], email='newemail@yahoo.fr')
        assert r.status_code == 200
