from sqlalchemy_utils import database_exists, drop_database, create_database


@rollback_on_exception
def create_bpr_database():
    if database_exists(db.engine.url):
        drop_database(db.engine.url)
    create_database(db.engine.url)
    db.create_all()
    db.session.commit()
