from datetime import datetime as dt, timedelta

from flask import render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from suslab.models import Product, Borrower, Lender
from suslab.database import db_commit
from .forms import ProductForm

library = Blueprint('library', __name__, url_prefix='/library',
                    template_folder='templates', static_folder='static')


@library.route('/')
def index():
    'Renders the library bulletin'
    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)


@library.route('/create-borrow')
@login_required
def create_borrow():
    'Renders a borrowing form'
    form = ProductForm()
    return render_template('library/create_borrow.html', form=form, homelink='/library/')


@library.route('/create-borrow', methods=['POST'])
@login_required
@db_commit(broadcast_data='library')
def create_borrow_post():
    'Accepts borrowing submissions'
    form, item = ProductForm(), None
    if form.validate_on_submit():
        borrower = current_user.borrower or Borrower(
            user = current_user,
        )
        needed_by = form.needed_by.data or dt.today() + timedelta(weeks=1)
        item = Product(
            name = form.name.data,
            description = form.description.data,
            borrower = borrower,
            duration = form.duration.data,
            needed_by = needed_by,
        )
    return item

@library.route('/edit/<int:id>')
@login_required
def edit(id):
    '''Renders an editing form for the given item

    id: int, the id of the item to be edited
    '''
    item = Product.query.get_or_404(id)
    needed_by = item.needed_by.strftime('%Y-%m-%d')

    form = ProductForm()

    if item.borrower.user != current_user or item.lender:
        return redirect(url_for('.index'))

    return render_template('library/edit_borrow.html', item=item, form=form,
                           needed_by=needed_by, homelink='/item/')


@library.route('/edit/<int:id>', methods=['POST'])
@login_required
@db_commit(broadcast_data='library')
def edit_post(id):
    '''Accepts editing submissions for the given item

    id: int, the id of the item to be edited
    '''
    item = Product.query.get_or_404(id)
    form = ProductForm()

    if item.borrower.user != current_user or item.lender:
        return redirect(url_for('.index'))

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.duration = form.duration.data
        item.needed_by = form.needed_by.data

    return item


# TODO: Add flash error for deleting
@library.route('/delete/<int:id>')
@login_required
@db_commit(broadcast_data='library', action='delete')
def delete(id):
    '''Deletes entry for the given item

    id: int, the id of the item to be edited
    '''
    item = Product.query.get_or_404(id)

    if item.borrower.user != current_user:
        return redirect(url_for('.index'))

    return item


# TODO: Add flash error for lending
@library.route('/lend/<int:id>')
@login_required
@db_commit(broadcast_data='library')
def lend(id):
    '''Creates a lend request for the given item

    id: int, the id of the item to be edited
    '''
    item = Product.query.get_or_404(id)

    if item.lender or item.borrower.user == current_user:
        return redirect(url_for('.index'))

    lender = current_user.lender or Lender(
        user = current_user,
    )
    item.lender = lender
    return item


# TODO: Add flash error for withdrawing
@library.route('/withdraw/<int:id>')
@login_required
@db_commit(broadcast_data='library')
def withdraw(id):
    '''Removes a lend request for the given item

    id: int, the id of the item to be edited
    '''
    item = Product.query.get_or_404(id)
    if not item.lender or item.lender.user != current_user:
        return redirect(url_for('.index'))

    item.lender = None
    return item
