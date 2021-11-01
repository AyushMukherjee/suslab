from flask import Flask, render_template, g
from flask_mail import Mail
from flask_security import Security
from flask_wtf.csrf import CSRFProtect

mail = Mail()


def create_app():
    '''Return the app by initializing components'''
    app = Flask(__name__)
    app.config.from_object('config')

    with app.app_context():
        from suslab.models import db
        from suslab.socket import socketio

        from suslab.users.controllers import get_user_datastore
        from suslab.users.forms import ExtendedRegisterForm

        from blueprints.library.controllers import library
        from blueprints.pool.controllers import pool
        from blueprints.info.controllers import info

        # create resources
        db.init_app(app)
        socketio.init_app(app)
        security = Security(app, get_user_datastore(), register_form=ExtendedRegisterForm)
        mail.init_app(app)
        csrf = CSRFProtect(app)

        # register blueprints
        app.register_blueprint(library)
        app.register_blueprint(pool)
        app.register_blueprint(info)

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

    return app
