from flask import Flask, render_template, g
from flask_mail import Mail
from flask_socketio import SocketIO, emit
from flask_security import Security
from flask_wtf.csrf import CSRFProtect


def create_app():
    '''Return the app by initializing components'''
    app = Flask(__name__)
    app.config.from_object('config')
    socketio = SocketIO(app)

    with app.app_context():
        from blueprints.library.controllers import library
        from blueprints.pool.controllers import pool
        from blueprints.info.controllers import info

        from suslab.users.controllers import get_user_datastore
        from suslab.users.forms import ExtendedRegisterForm
        from suslab.users.models import db

        # register blueprints
        app.register_blueprint(library)
        app.register_blueprint(pool)
        app.register_blueprint(info)

        db.init_app(app)
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
        

        def library_data():
            socketio.emit('pong library', 'you have reached the library')


        def pool_data():
            socketio.emit('pong pool', 'you have reached the pool')

    return app, socketio
