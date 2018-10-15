from app.model import rollback_on_exception, User, Accomodation


@rollback_on_exception
def user(id_):
    try:
        user = User.query.filter_by(id=id_).one()
    except DataError:
        raise ValidationError('Not a valid integer value')
    except NoResultFound:
        raise ValidationError('User with id: {} does not exist'.format(id_))
    return user


@rollback_on_exception
def accomodation(id_):
    try:
        accomodation = Accomodation.query.filter_by(id=id_).one()
    except DataError:
        raise ValidationError('Not a valid integer value')
    except NoResultFound:
        raise ValidationError('Accomodation with id: {} does not exist'.format(id_))
    return accomodation


@rollback_on_exception
def notification(id_):
    pass


def validate_geometry(value):
    try:
        tested_shape = shape(value)
    except:
        raise ValidationError('incorrect geometry')
    if tested_shape.is_valid is False:
        raise ValidationError('invalid shape: {}'.format(value))
    return tested_shape.is_valid
