from app.model import rollback_on_exception, User


@rollback_on_exception
def user(user_id):
    try:
        user = User.query.filter_by(id=user_id).one()
    except DataError:
        raise ValidationError('Not a valid integer value')
    except NoResultFound:
        raise ValidationError('User with id: {} does not exist'.format(id_))
    return user


def validate_geometry(value):
    try:
        tested_shape = shape(value)
    except:
        raise ValidationError('incorrect geometry')
    if tested_shape.is_valid is False:
        raise ValidationError('invalid shape: {}'.format(value))
    return tested_shape.is_valid
