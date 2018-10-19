from sqlalchemy_utils import database_exists, drop_database, create_database
from app.common import app_context
from app.resources.user import create_user
from app.model import rollback_on_exception, db


@rollback_on_exception
def drop_and_create_database():
    if database_exists(db.engine.url):
        drop_database(db.engine.url)
    create_database(db.engine.url)
    db.create_all()
    db.session.commit()


def init_database():
    with app_context:
        drop_and_create_database()
        create_user(username='admin', password='default')


if __name__ == '__main__':
    init_database()
