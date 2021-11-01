from flask_security import SQLAlchemyUserDatastore


def get_user_datastore():
    from suslab.models import User, Role, db
    return SQLAlchemyUserDatastore(db, User, Role)
