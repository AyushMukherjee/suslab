'This module implements socket connections'

from datetime import datetime as dt
from flask_socketio import SocketIO

from .models import Product, Pool

__all__ = ['broadcast']

socketio = SocketIO()

@socketio.on('library', namespace='/library')
def _library():
    'Broadcast library data'
    socketio.emit(
        'library',
        (
            f'you have reached the library at {dt.now().time()}',
            {'data': [item.to_json(max_nesting=4) for item in Product.query]}
        )
    )

@socketio.on('pool', namespace='/pool')
def _pool():
    'Broadcast pool spots data'
    socketio.emit(
        'pool',
        (
            f'you have reached the pool at {dt.now().time()}',
            {'data': [pool.to_json(max_nesting=4) for pool in Pool.query]},
        )
    )

def broadcast(broadcast_data=None):
    '''Implements broadcast switching

    broadcast_data: string, data key to be broadcast
    '''
    if broadcast_data == 'library':
        _library()
    if broadcast_data == 'pool':
        _pool()
