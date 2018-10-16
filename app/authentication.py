from flask_httpauth import HTTPBasicAuth
from flask import g, abort
from app.model import User
from werkzeug.security import check_password_hash

auth = HTTPBasicAuth()


def verify_password(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    return None


@auth.verify_password
def verify_user_password(username, password):
    user = verify_password(username, password)
    if user is not None:
        g.user = user
        return True
    else:
        return False
