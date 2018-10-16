import unittest
from app.api import app as raw_app
from sqlalchemy_utils import database_exists, drop_database, create_database
from app.tests.client import Client
from app.model import db


class BaseTestCase(unittest.TestCase):
    raw_app = raw_app

    @classmethod
    def setUpClass(cls):
        cls.raw_app.config.update({
            'SQLALCHEMY_DATABASE_URI': 'sqlite://',
        })

        cls.raw_app.testing = True
        cls.test_app = cls.raw_app.test_client()
        cls.app_context = cls.raw_app.app_context()
        cls.app_context.push()
        if database_exists(db.engine.url):
            drop_database(db.engine.url)
        create_database(db.engine.url)

    @property
    def client(self):
        return Client(self.username, self.password, test_app=self.test_app, app=self.raw_app)

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    def setUp(self):
        db.drop_all()
        db.create_all()

    def tearDown(self):
        db.session.rollback()
        db.drop_all()
