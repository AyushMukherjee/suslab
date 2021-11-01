from flask import g
from suslab import create_app

handler, socketio = create_app()

if __name__ == '__main__':
    socketio.run(handler, debug=True)
