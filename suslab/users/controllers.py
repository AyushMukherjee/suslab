from flask import request, render_template, url_for, redirect
from flask_security import SQLAlchemyUserDatastore


def get_user_datastore():
    from suslab.users.models import User, Role
    from suslab import db

    return SQLAlchemyUserDatastore(db, User, Role)
