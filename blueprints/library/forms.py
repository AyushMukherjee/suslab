from flask_wtf import FlaskForm
from wtforms.fields import StringField, IntegerField, TextAreaField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class ProductForm(FlaskForm):
    name = StringField(
        'name',
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
    needed_by = DateField(
        'needed_by',
        validators=[],
    )
    submit = SubmitField('Create New Request')
