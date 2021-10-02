from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user

pool = Blueprint('pool', __name__, url_prefix='/pool')

def _db_conn():
    from suslab.users.models import Pool, Pooler
    from suslab import db

    return Pool, Pooler, db

@pool.route('/')
def index():
    Pool, Pooler, db = _db_conn()
    form = ProductForm()

    # Verify the form
    if form.validate_on_submit():
        pooler = Pooler(
            user = current_user,
        )
        item = Product(
            name=form.item.data,
            description=form.description.data,
            borrower = borrower,
        )
        try:
            db.session.add(borrower)
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('library.index'))
        except:
            return 'There was an issue adding your item'

    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)