from flask import request, render_template, url_for, redirect
from flask_security import SQLAlchemyUserDatastore
from suslab import app, db

def get_user_datastore():
    from suslab.users.models import User, Role
    from suslab import db

    return SQLAlchemyUserDatastore(db, User, Role)

@app.route('/userinfo')
def userinfo():
    return render_template('UserPro.html')


@app.route('/userinfoedit')
def editdetails():
    return render_template('UserProEdit.html')