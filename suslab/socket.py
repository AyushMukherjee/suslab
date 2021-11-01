from datetime import datetime as dt
from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on('library', namespace='/library')
def library():
    socketio.emit('library', f'you have reached the library at {dt.now().time()}')

@socketio.on('pool', namespace='/pool')
def pool():
    socketio.emit('pool', f'you have reached the pool at {dt.now().time()}')

def broadcast(broadcast_data=None):
    if broadcast_data == 'library':
        library()
    if broadcast_data == 'pool':
        print('trying')
        pool()
