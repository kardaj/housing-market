from webargs import fields
from webargs.flaskparser import use_kwargs
from app import parse
from marshmallow import validate
from app.resources import DefaultSchema, DefaultResource
from app.model import db, User, rollback_on_exception
from flask import g
from werkzeug.security import generate_password_hash


class ArgsUserPut(DefaultSchema):
    user = fields.Function(required=True, deserialize=parse.user, load_from='user_id', location='view_args')
    username = fields.String(location='json')
    email = fields.String(location='json', validate=validate.Email())
    notify = fields.Boolean(location='json')


def get_user(user):
    return {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'notify': user.notify
    }


def create_user(username, password, email=None):
    password_hash = generate_password_hash(password)
    user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(user)
    db.session.commit()
    return user


class UserResource(DefaultResource):
    @rollback_on_exception
    @use_kwargs(ArgsUserPut)
    def put(self, user, **kwargs):
        assert g.user.id == user.id
        return self.jsonify(get_user(g.user))


class AuthResource(DefaultResource):
    def get(self):
        return self.jsonify(get_user(g.user))
