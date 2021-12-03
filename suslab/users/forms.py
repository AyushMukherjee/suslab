'This module extends the security forms from flask-security'

from flask_security import RegisterForm
from flask_security.forms import Length
from wtforms import StringField
from flask_wtf import FlaskForm
from wtforms import validators
from wtforms.fields.core import DateField, IntegerField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms_alchemy import ModelForm








programme_choices = [
    ('Mathematics', 'Mathematics'),
    ('Biology', 'Biology'),
    ('Physics', 'Physics'),
    ('BA Economics', 'BA Economics'),    
    ('BA  Humanities', 'BA  Humanities'),
    ('BA Literature', 'BA Literature'),
    ('MA Economics', 'MA Economics'),
    ('MA Development', 'MA Developments'),
    ('MA Education', 'MA Education'),
    ('Others', 'Others'),

]




class ExtendedRegisterForm(RegisterForm):
    'Extends the registration form to ask for user name'
    name = StringField('Name', [DataRequired()])





class editUserInfoForm(FlaskForm):
    name = StringField(
        'name', 
        validators=[
            DataRequired(message="Name can't be empty!"), 
            Length(max=100, message=("Name is too lengthy!"))])

    contact_number = StringField(
        'contanct_number', 
        validators=[
            DataRequired(message="Contact number is necessary!"),
            # NumberRange(min=10, max=12, message="Invalid Contact!")
        ])
    programme_name = SelectField("Programme Name", choices=programme_choices)
    address = StringField('address',validators=None)
    dob = DateField('dob',validators=None)
    gender = StringField('gender',validators=None)
    submit = SubmitField("Edit user data")



