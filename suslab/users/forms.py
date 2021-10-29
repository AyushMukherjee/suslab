from flask_security import RegisterForm
from wtforms import StringField
from wtforms.validators import DataRequired

class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])
