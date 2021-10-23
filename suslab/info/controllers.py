from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from suslab.library.forms import ProductForm


info = Blueprint('info', __name__, url_prefix='/')


@info.route('/contact')
def contact():
    # Verify the form
    # if form.validate_on_submit():
    #     borrower = Borrower(
    #         user = current_user,
    #     )
    #     item = Product(
    #         name=form.item.data,
    #         description=form.description.data,
    #         borrower = borrower,
    #     )
    #     try:
    #         db.session.add(borrower)
    #         db.session.add(item)
    #         db.session.commit()
    #         return redirect(url_for('library.index'))
    #     except:
    #         return 'There was an issue adding your item'

    return render_template('info/contact.html')
