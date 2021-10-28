from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from .forms import ProductForm


library = Blueprint('library', __name__, url_prefix='/library',
                    template_folder='templates', static_folder='static')


def _db_conn():
    from suslab.users.models import Product, Borrower, Lender
    from suslab import db

    return Product, Borrower, Lender, db


@library.route('/')
def index():
    Product, *_ = _db_conn()

    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)


@library.route('/create-borrow-request', methods=['GET', 'POST'])
@login_required
def create_borrow_request():
    Product, Borrower, _, db = _db_conn()
    form = ProductForm()

    # Verify the form
    if form.validate_on_submit():
        borrower = current_user.borrower or Borrower(
            user = current_user,
        )
        item = Product(
            name = form.item.data,
            description = form.description.data,
            borrower = borrower,
            duration = form.duration.data,
        )
        try:
            db.session.add_all([borrower, item])
            db.session.commit()
            return redirect(url_for('.index'))
        except Exception:
            return 'There was an issue adding your item'

    return render_template('library/create_borrow_request.html', form=form, homelink='/library/')


# TODO: Add flash error for deleting
@library.route('/delete/<int:id>')
@login_required
def delete(id):
    Product, _, _, db = _db_conn()
    item = Product.query.get_or_404(id)

    if item.borrower.user != current_user:
        return redirect(url_for('.index'))

    try:
        db.session.delete(item)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem deleting that item'


# TODO: Add flash error for lending
@library.route('/lend/<int:id>')
@login_required
def lend(id):
    Product, _, Lender, db = _db_conn()
    item = Product.query.get_or_404(id)
    
    if item.lender or item.borrower.user == current_user:
        return redirect(url_for('.index'))

    lender = current_user.lender or Lender(
        user = current_user,
    )
    item.lender = lender

    try:
        db.session.add_all([lender, item])
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem lending'


# TODO: Add flash error for withdrawing
@library.route('/withdraw/<int:id>')
@login_required
def withdraw(id):
    Product, _, Lender, db = _db_conn()
    item = Product.query.get_or_404(id)
    if not item.lender or item.lender.user != current_user:
        return redirect(url_for('.index'))
    
    item.lender = None

    try:
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.index'))
    except:
        return 'There was a problem withdrawing'
