'This module creates simple database utils'

from functools import wraps

from flask import redirect, url_for

from .models import db
from .socket import broadcast

def db_commit(broadcast_data=None, action='add'):
    'Decorates functions to commit to the database and broadcast data if needed'
    def decorator(func):
        'Outer decorator function'
        @wraps(func)
        def decorated_function(*args, **kwargs):
            'Inner decorator function'
            entry = func(*args, **kwargs)
            try:
                if action == 'add':
                    db.session.add(entry)
                elif action == 'delete':
                    db.session.delete(entry)
                db.session.commit()
                broadcast(broadcast_data)
                return redirect(url_for('.index'))
            except Exception as error:
                return f'There is some error. Please send this to the admin:\n{error}'
        return decorated_function
    return decorator
