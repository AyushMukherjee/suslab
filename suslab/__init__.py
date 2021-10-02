from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_wtf.csrf import CSRFProtect

from suslab.library.controllers import library
from suslab.pool.controllers import pool
from suslab.users.controllers import get_user_datastore

app = Flask(__name__)
app.config.from_object('config')

# register apps
app.register_blueprint(library)
app.register_blueprint(pool)

db = SQLAlchemy(app)
security = Security(app, get_user_datastore())

csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


def get_app():
    '''Return the app by initializing components'''
    return app
