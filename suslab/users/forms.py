'This module extends the security forms from flask-security'

from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    'Extends the registration form to ask for user name'
    name = StringField('Name', [DataRequired()])
