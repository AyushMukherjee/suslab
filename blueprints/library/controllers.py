from datetime import datetime as dt, timedelta

from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_security.decorators import login_required

from suslab.models import db, Product, Borrower, Lender
from suslab.socket import broadcast
from .forms import ProductForm

library = Blueprint('library', __name__, url_prefix='/library',
                    template_folder='templates', static_folder='static')


@library.route('/')
def index():
    items = Product.query.order_by(Product.date_created).all()
    return render_template('library/index.html', items=items)


@library.route('/create-borrow', methods=['GET', 'POST'])
@login_required
def create_borrow():
    form = ProductForm()

    # Verify the form
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
        try:
            db.session.add(item)
            db.session.commit()
            broadcast('library')
            return redirect(url_for('.index'))
        except Exception as e:
                return f'There is some error. Please send this to the admin:\n{e}'

    return render_template('library/create_borrow.html', form=form, homelink='/library/')


@library.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    item = Product.query.get_or_404(id)
    needed_by = item.needed_by.strftime('%Y-%m-%d')

    form = ProductForm()

    if item.borrower.user != current_user or item.lender:
        return redirect(url_for('.index'))

    if form.validate_on_submit():
        item.name = form.name.data
        item.description = form.description.data
        item.duration = form.duration.data
        item.needed_by = form.needed_by.data

        try:
            db.session.add(item)
            db.session.commit()
            broadcast('library')
            return redirect(url_for('.index'))
        except:
            return 'There was an issue editing your item'

    return render_template('library/edit_borrow.html', item=item, form=form,
                           needed_by=needed_by, homelink='/item/')


# TODO: Add flash error for deleting
@library.route('/delete/<int:id>')
@login_required
def delete(id):
    item = Product.query.get_or_404(id)

    if item.borrower.user != current_user:
        return redirect(url_for('.index'))

    try:
        db.session.delete(item)
        db.session.commit()
        broadcast('library')
        return redirect(url_for('.index'))
    except Exception as e:
        print(e)
        return 'There was a problem deleting that item'


# TODO: Add flash error for lending
@library.route('/lend/<int:id>')
@login_required
def lend(id):
    item = Product.query.get_or_404(id)
    
    if item.lender or item.borrower.user == current_user:
        return redirect(url_for('.index'))

    lender = current_user.lender or Lender(
        user = current_user,
    )
    item.lender = lender

    try:
        db.session.add(item)
        db.session.commit()
        broadcast('library')
        return redirect(url_for('.index'))
    except:
        return 'There was a problem lending'


# TODO: Add flash error for withdrawing
@library.route('/withdraw/<int:id>')
@login_required
def withdraw(id):
    item = Product.query.get_or_404(id)
    if not item.lender or item.lender.user != current_user:
        return redirect(url_for('.index'))
    
    item.lender = None

    try:
        db.session.add(item)
        db.session.commit()
        broadcast('library')
        return redirect(url_for('.index'))
    except:
        return 'There was a problem withdrawing'
