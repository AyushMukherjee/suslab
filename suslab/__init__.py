from flask import Flask, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from suslab.library.controllers import library

app = Flask(__name__)
app.config.from_object('config')
app.register_blueprint(library)

db = SQLAlchemy(app)

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
