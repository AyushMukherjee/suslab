from suslab import create_app
from suslab.socket import socketio

handler = create_app()

if __name__ == '__main__':
    socketio.run(handler, debug=True)
