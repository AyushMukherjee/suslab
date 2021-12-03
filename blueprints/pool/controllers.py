'This module implements the routes for the pool spots app'

from datetime import datetime as dt

from flask import render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from suslab.models import Pool, Pooler, Signup
from suslab.database import db_commit
from .forms import PoolForm

pool = Blueprint('pool', __name__, url_prefix='/pool',
                 template_folder='templates', static_folder='static')


@pool.route('/')
def index():
    'Renders the pool spots bulletin'
    pools = Pool.query.order_by(Pool.time).all()
    return render_template('pool/index.html', pools=pools)


@pool.route('/api/data')
def data():
    return {'data': [pool.to_json(max_nesting=4) for pool in Pool.query]}


@pool.route('/create-pool')
@login_required
def create_pool():
    'Renders a pool request form'
    form = PoolForm()    
    return render_template('pool/create_pool.html', form=form, homelink='/pool/')


@pool.route('/create-pool', methods=['POST'])
@login_required
@db_commit(broadcast_data='pool')
def create_pool_post():
    'Accepts pool requests'
    form, pool_ = PoolForm(), None
    if form.validate_on_submit():
        pool_datetime = dt.strptime(f'{form.date.data} {form.time.data}', '%Y-%m-%d %H:%M:%S')
        pooler = current_user.pooler or Pooler(
            user = current_user,
        )
        pool_ = Pool(
            from_ = form.from_.data,
            to_ = form.to_.data,
            time = pool_datetime,
            vehicle = form.vehicle.data,
            spots = form.spots.data,
            pooler = pooler,
        )
    return pool_


@pool.route('/edit/<int:pool_id>')
@login_required
def edit(pool_id):
    '''Renders an editing form for the given pool

    pool_id: int, the id of the pool to be edited
    '''
    pool_ = Pool.query.get_or_404(pool_id)
    pool_date, pool_time = pool_.time.strftime('%Y-%m-%d'), pool_.time.strftime('%H:%M')

    form = PoolForm()

    if pool_.pooler.user != current_user or pool_.signups:
        return redirect(url_for('.index'))

    return render_template('pool/edit_pool.html', pool=pool_, form=form,
                           homelink='/pool/', pool_date=pool_date, pool_time=pool_time)


@pool.route('/edit/<int:pool_id>', methods=['POST'])
@login_required
@db_commit(broadcast_data='pool')
def edit_post(pool_id):
    '''Accepts editing submissions for the given pool

    pool_id: int, the id of the pool to be edited
    '''
    pool_ = Pool.query.get_or_404(pool_id)
    form = PoolForm()

    if pool_.pooler.user != current_user or pool_.signups:
        return redirect(url_for('.index'))

    if form.validate_on_submit():
        pool_datetime = dt.strptime(f'{form.date.data} {form.time.data}', '%Y-%m-%d %H:%M:%S')

        pool_.from_ = form.from_.data
        pool_.to_ = form.to_.data
        pool_.time = pool_datetime
        pool_.vehicle = form.vehicle.data
        pool_.spots = form.spots.data

    return pool_


# TODO: Add flash error for deleting
@pool.route('/delete/<int:pool_id>')
@login_required
@db_commit(broadcast_data='pool', action='delete')
def delete(pool_id):
    '''Deletes entry for given pool

    pool_id: int, the id of the pool to be deleted
    '''
    pool_ = Pool.query.get_or_404(pool_id)

    if pool_.pooler.user != current_user:
        return redirect(url_for('.index'))

    return pool_


# TODO: Add flash error for signing up
@pool.route('/signup/<int:pool_id>')
@login_required
@db_commit(broadcast_data='pool')
def signup(pool_id):
    '''Creates a signup request for given pool

    pool_id: int, the id of the pool to be signed up for
    '''
    pool_ = Pool.query.get_or_404(pool_id)

    signup_ = current_user.signup or Signup(
        user = current_user,
    )
    if len(pool_.signups or []) >= pool_.spots \
        or signup_ in pool_.signups \
        or pool_.pooler.user == current_user:
        # return a redirect here
        return redirect(url_for('.index'))

    pool_.signups = (pool_.signups or []) + [signup_]
    return pool


# TODO: Add flash error for withdrawing
@pool.route('/withdraw/<int:pool_id>')
@login_required
@db_commit(broadcast_data='pool')
def withdraw(pool_id):
    '''Removes a signup request for given pool

    pool_id: int, the id of the pool to be signed up for
    '''
    pool_ = Pool.query.get_or_404(pool_id)
    signup_ = current_user.signup or Signup(
        user = current_user,
    )

    if signup_ not in (pool_.signups or []):
        return redirect(url_for('.index'))

    pool_.signups.remove(signup_)
    return pool_
