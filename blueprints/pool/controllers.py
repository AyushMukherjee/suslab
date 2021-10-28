from datetime import datetime as dt

from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from .forms import PoolForm

pool = Blueprint('pool', __name__, url_prefix='/pool',
                 template_folder='templates', static_folder='static')


def _db_conn():
    from suslab.users.models import Pool, Pooler, Signup
    from suslab import db

    return Pool, Pooler, Signup, db


@pool.route('/')
def index():
    Pool, *_ = _db_conn()

    pools = Pool.query.order_by(Pool.time).all()
    return render_template('pool/index.html', pools=pools)


@pool.route('/create-pool', methods=['GET', 'POST'])
@login_required
def create_pool():
    Pool, Pooler, _, db = _db_conn()
    form = PoolForm()

    # Verify the form
    if form.validate_on_submit():
        pool_datetime = dt.strptime(f'{form.date.data} {form.time.data}', '%Y-%m-%d %H:%M:%S')
        pooler = current_user.pooler or Pooler(
            user = current_user,
        )
        pool = Pool(
            from_ = form.from_.data,
            to_ = form.to_.data,
            time = pool_datetime,
            vehicle = form.vehicle.data,
            spots = form.spots.data,
            pooler = pooler,
        )
        try:
            db.session.add(pool)
            db.session.commit()
            return redirect(url_for('.index'))
        except:
            return 'There was an issue adding your item'
    
    return render_template('pool/create_pool.html', form=form, homelink='/pool/')


# TODO: Add flash error for deleting
@pool.route('/delete/<int:id>')
@login_required
def delete(id):
    Pool, _, _, db = _db_conn()
    pool = Pool.query.get_or_404(id)

    if pool.pooler.user != current_user:
        return redirect(url_for('.index'))

    try:
        db.session.delete(pool)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem deleting that pool'


# TODO: Add flash error for signing up
@pool.route('/signup/<int:id>')
@login_required
def signup(id):
    Pool, _, Signup, db = _db_conn()
    pool = Pool.query.get_or_404(id)

    signup = current_user.signup or Signup(
        user = current_user,
    )
    if len(pool.signups or []) >= pool.spots or signup in pool.signups or pool.pooler.user == current_user:
        return redirect(url_for('.index'))

    pool.signups = (pool.signups or []) + [signup]

    try:
        db.session.add(pool)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem signing up'


# TODO: Add flash error for withdrawing
@pool.route('/withdraw/<int:id>')
@login_required
def withdraw(id):
    Pool, _, Signup, db = _db_conn()
    pool = Pool.query.get_or_404(id)
    signup = current_user.signup or Signup(
        user = current_user,
    )

    if signup not in (pool.signups or []):
        return redirect(url_for('.index'))

    pool.signups.remove(signup)

    try:
        db.session.add(pool)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem withdrawing'
