from flask import Flask, render_template
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security
from flask_wtf.csrf import CSRFProtect

from suslab.library.controllers import library
from blueprints.pool.controllers import pool
from suslab.info.controllers import info
from suslab.users.controllers import get_user_datastore
from suslab.users.forms import ExtendedRegisterForm

app = Flask(__name__)
app.config.from_object('config')

# register apps
app.register_blueprint(library)
app.register_blueprint(pool)
app.register_blueprint(info)

db = SQLAlchemy(app)
security = Security(app, get_user_datastore(), register_form=ExtendedRegisterForm)
mail = Mail(app)

csrf = CSRFProtect(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


@app.context_processor
def utility_processor():
    def user_avatar(user_name, category='croodles-neutral'):
        user_name_clean = '-'.join(user_name.split())
        return f'https://avatars.dicebear.com/api/{category}/{user_name_clean}.svg'
    return dict(user_avatar=user_avatar)


def get_app():
    '''Return the app by initializing components'''
    return app
