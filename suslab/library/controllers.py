from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from suslab.library.forms import ProductForm


library = Blueprint('library', __name__, url_prefix='/library')


def _db_conn():
    from suslab.users.models import Product
    from suslab import db

    return Product, db


@library.route('/', methods=['GET', 'POST'])
def index():
    Product, db = _db_conn()
    form = ProductForm()

    # Verify the form
    if form.validate_on_submit():
        item = Product(
            name=form.item.data,
            description=form.description.data,
            user=current_user,
        )
        try:
            db.session.add(item)
            db.session.commit()
            return redirect(url_for('library.index'))
        except:
            return 'There was an issue adding your item'

    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)


@library.route('/delete/<int:id>')
def delete(id):
    Product, db = _db_conn()
    item = Product.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('library.index'))
    except:
        return 'There was a problem deleting that task'

@library.route('/admin')
def admin():
    Product, db = _db_conn()
    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/admin_dummy.html', items=items)