from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, TextAreaField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    item = StringField(
        'item',
        validators=[
            DataRequired(message='Please specify an item name'),
            Length(min=1, max=128, message='Please specify a valid item'),
        ]
    )
    description = TextAreaField(
        'description',
        validators=[
            DataRequired(message='Please specify an item description'),
            Length(min=32, max=128, message='Please specify a valid description'),
        ]
    )
    duration = IntegerField(
        'duration',
        validators=[
            DataRequired(message='Please specify a borrow duration'),
            NumberRange(min=1, max=14, message='Please specify a number between 1 and 14'),
        ]
    )
    submit = SubmitField('Create New Request')
