from sqlalchemy_utils import database_exists, drop_database, create_database
from app.common import flask_app_context
from app.resources.user import create_user
from app.resources.listing import bulk_insert_listings
from app.model import rollback_on_exception, db
from app.conf import PROJECT_DIR
import os
import csv


@rollback_on_exception
def drop_and_create_database():
    if database_exists(db.engine.url):
        drop_database(db.engine.url)
    create_database(db.engine.url)
    db.drop_all()
    db.create_all()
    db.session.commit()


def init_database():
    with flask_app_context:
        drop_and_create_database()
        create_user(username='admin', password='default')
        with open(os.path.join(PROJECT_DIR, 'app/common/listings.csv')) as csvfile:
            reader = csv.DictReader(csvfile)
            bulk_insert_listings(list(reader))


if __name__ == '__main__':
    init_database()
