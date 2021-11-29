from flask_security import RegisterForm
from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired
from wtforms_alchemy import ModelForm
# from .models import User as userr



class ExtendedRegisterForm(RegisterForm):
    name = StringField('Name', [DataRequired()])


class editUserInfoForm(FlaskForm):
    name = StringField('name', validators=None)
    # roles = SelectField("roles", choices=[])
    contact_number = IntegerField('contanct_number', validators=None)
    programme_name = StringField('programme_name', validators=None)
    address = StringField('address',validators=None)
    dob = DateField('dob',validators=None)
    gender = StringField('gender',validators=None)
    submit = SubmitField("Edit user data")


