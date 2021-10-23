from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Length, Email


class ContactForm(FlaskForm):
    name = StringField(
        'Name',
        validators=[
            InputRequired(message='Please provide your name'),
        ]
    )
    email = StringField(
        'Email',
        validators=[
            InputRequired(message='Please provide an email address'),
            Email(message='Please enter a valid email address'),
        ]
    )
    message = TextAreaField(
        'Message',
        validators=[
            InputRequired(message='You must write a message'),
            Length(min=32, message='Message must be more than 32 characters in length')
        ]
    )
    submit = SubmitField('Email Us')