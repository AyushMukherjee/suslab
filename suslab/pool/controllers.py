from datetime import datetime as dt

from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from suslab.pool.forms import PoolForm

pool = Blueprint('pool', __name__, url_prefix='/pool')

def _db_conn():
    from suslab.users.models import Pool, Pooler, Signup
    from suslab import db

    return Pool, Pooler, Signup, db

@pool.route('/', methods=['GET', 'POST'])
def index():
    Pool, _, _, _ = _db_conn()

    pools = Pool.query.order_by(Pool.time).all()
    return render_template('pool/index.html', pools=pools)

@pool.route('/create-pool/', methods=['GET', 'POST'])
@login_required
def create_pool():
    if not current_user.is_authenticated:
        redirect(url_for('pool.index'))

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
            pooler = pooler,
        )
        try:
            if not current_user.pooler:
                db.session.add(pooler)
            db.session.add(pool)
            db.session.commit()
            return redirect(url_for('pool.index'))
        except:
            return 'There was an issue adding your item'
    
    return render_template('pool/create_pool.html', form=form)


@pool.route('/signup/<int:id>')
def signup(id):
    Pool, _, Signup, db = _db_conn()
    pool = Pool.query.get_or_404(id)
    signup = current_user.signup or Signup(
        user = current_user,
    )
    print(signup)
    pool.signups = [signup]
    print(pool)
    print(not current_user.signup)

    try:
        if not current_user.signup:
            db.session.add(signup)
        db.session.commit()
        return redirect(url_for('pool.index'))
    except:
        return 'There was a problem signing up'
