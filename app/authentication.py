from flask_httpauth import HTTPBasicAuth
from flask import g, abort
from app.model import User

auth = HTTPBasicAuth()


def verify_password(email, password):
    user = User.query.filter_by(email=email).first()
    if user and not user.is_deleted and user.verify_password(password):
        if user.is_active:
            return user
        else:
            abort(403)
    return False


@auth.verify_password
def verify_user_password(email, password):
    login_result = verify_password(email, password)
    if login_result:
        g.user = login_result
        return True
    else:
        return False
