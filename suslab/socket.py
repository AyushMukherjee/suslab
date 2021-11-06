'This module implements socket connections'

from datetime import datetime as dt
from flask_socketio import SocketIO, Namespace, emit

from .models import Product, Pool, Borrower, Lender, User, db

socketio = SocketIO()


def __data():
    lender_subquery = db.session.query(Product.id)\
        .join(Lender, Lender.id==Product.lender_id, isouter=True)\
        .join(User, User.id==Lender.user_id, isouter=True)\
        .add_columns(User.name.label('lender_name'))\
        .subquery()
    query = Product.query\
        .join(Borrower, Borrower.id==Product.borrower_id)\
        .join(User, User.id==Borrower.user_id)\
        .add_columns(User.name.label('borrower_name'))\
        .join(lender_subquery, lender_subquery.c.id==Product.id)\
        .add_columns(lender_subquery.c.lender_name.label('lender_name'))
    return {
        'data': [{
            'id': item.Product.id,
            'name': item.Product.name,
            'description': item.Product.description,
            'duration': item.Product.duration,
            'needed_by': item.Product.needed_by.strftime('%Y-%m-%d'),
            'borrower': item.borrower_name,
            'lender': item.lender_name,
        } for item in query.all()]
    }


def _library():
    'Broadcast library items data'
    socketio.emit('library', __data(), namespace='/library')


@socketio.on('connect', namespace='/library')
def _library_connect(auth):
    'Broadcast library items data'
    emit('library', __data())


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
