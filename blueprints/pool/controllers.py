from datetime import datetime as dt

from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from suslab.models import Pool, Pooler, Signup
from suslab.database import db_commit
from .forms import PoolForm

pool = Blueprint('pool', __name__, url_prefix='/pool',
                 template_folder='templates', static_folder='static')


@pool.route('/')
def index():
    pools = Pool.query.order_by(Pool.time).all()
    return render_template('pool/index.html', pools=pools)


@pool.route('/api/data')
def data():
    return {'data': [pool.to_json(max_nesting=4) for pool in Pool.query]}


@pool.route('/create-pool')
@login_required
def create_pool():
    form = PoolForm()    
    return render_template('pool/create_pool.html', form=form, homelink='/pool/')


@pool.route('/create-pool', methods=['POST'])
@login_required
@db_commit(broadcast_data='pool')
def create_pool_post():
    form, pool = PoolForm(), None
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
    return pool


@pool.route('/edit/<int:id>')
@login_required
def edit(id):
    pool = Pool.query.get_or_404(id)
    pool_date, pool_time = pool.time.strftime('%Y-%m-%d'), pool.time.strftime('%H:%M')

    form = PoolForm()

    if pool.pooler.user != current_user or pool.signups:
        return redirect(url_for('.index'))

    return render_template('pool/edit_pool.html', pool=pool, form=form,
                           homelink='/pool/', pool_date=pool_date, pool_time=pool_time)


@pool.route('/edit/<int:id>', methods=['POST'])
@login_required
@db_commit(broadcast_data='pool')
def edit_post(id):
    pool = Pool.query.get_or_404(id)
    form = PoolForm()

    if pool.pooler.user != current_user or pool.signups:
        return redirect(url_for('.index'))

    if form.validate_on_submit():
        pool_datetime = dt.strptime(f'{form.date.data} {form.time.data}', '%Y-%m-%d %H:%M:%S')

        pool.from_ = form.from_.data
        pool.to_ = form.to_.data
        pool.time = pool_datetime
        pool.vehicle = form.vehicle.data
        pool.spots = form.spots.data

    return pool


# TODO: Add flash error for deleting
@pool.route('/delete/<int:id>')
@login_required
@db_commit(broadcast_data='pool', action='delete')
def delete(id):
    pool = Pool.query.get_or_404(id)

    if pool.pooler.user != current_user:
        return redirect(url_for('.index'))

    return pool


# TODO: Add flash error for signing up
@pool.route('/signup/<int:id>')
@login_required
@db_commit(broadcast_data='pool')
def signup(id):
    pool = Pool.query.get_or_404(id)

    signup = current_user.signup or Signup(
        user = current_user,
    )
    if len(pool.signups or []) >= pool.spots or signup in pool.signups or pool.pooler.user == current_user:
        return redirect(url_for('.index'))

    pool.signups = (pool.signups or []) + [signup]
    return pool


# TODO: Add flash error for withdrawing
@pool.route('/withdraw/<int:id>')
@login_required
@db_commit(broadcast_data='pool')
def withdraw(id):
    pool = Pool.query.get_or_404(id)
    signup = current_user.signup or Signup(
        user = current_user,
    )

    if signup not in (pool.signups or []):
        return redirect(url_for('.index'))

    pool.signups.remove(signup)
    return pool
