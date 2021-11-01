from flask_socketio import SocketIO, emit

socketio = SocketIO()

@socketio.on('library', namespace='/library')
def library():
    socketio.emit('library', 'you have reached the library')
