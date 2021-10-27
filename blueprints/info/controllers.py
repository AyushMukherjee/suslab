from flask import request, render_template, Blueprint, url_for, redirect
from flask_security import current_user
from flask_mail import Message

from .forms import ContactForm


info = Blueprint('info', __name__, url_prefix='/',
                 template_folder='templates', static_folder='static')


def _mailer_conn():
    from suslab import mail
    return mail


@info.route('/contact', methods=['GET', 'POST'])
def contact():
    mail = _mailer_conn()
    form = ContactForm()

    # Verify the form
    if form.validate_on_submit():
        message = Message(
            recipients=['suslab@example.com'],
            subject=f'Message from {form.name.data}',
            body=form.message.data,
        )
        mail.send(message)

    return render_template('info/contact.html', form=form)
