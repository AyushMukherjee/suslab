from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from .forms import ProductForm


library = Blueprint('library', __name__, url_prefix='/library',
                    template_folder='templates', static_folder='static')


def _db_conn():
    from suslab.users.models import Product, Borrower, Lender
    from suslab import db

    return Product, Borrower, Lender, db


@library.route('/', methods=['GET', 'POST'])
def index():
    Product, Borrower, _, db = _db_conn()
    form = ProductForm()

    # Verify the form
    if form.validate_on_submit():
        borrower = Borrower(
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
            return redirect(url_for('.index'))
        except:
            return 'There was an issue adding your item'

    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)


@library.route('/delete/<int:id>')
def delete(id):
    Product, Borrower, _, db = _db_conn()
    item = Product.query.get_or_404(id)

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem deleting that task'


@library.route('/lend/<int:id>')
def lend(id):
    Product, Borrower, Lender, db = _db_conn()
    item = Product.query.get_or_404(id)
    borrower = item.borrower
    lender = Lender(
        user = current_user,
        borrowers = [borrower],
    )

    item.lender = lender

    try:
        db.session.add(lender)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem deleting that task'
