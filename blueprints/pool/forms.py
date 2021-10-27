from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TimeField
from wtforms.fields.core import IntegerField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class PoolForm(FlaskForm):
    from_ = StringField(
      'from_',
      validators=[
        DataRequired(message='Please specify a pool source'),
        Length(min=1, max=32, message='Please specify a valid source'),
      ]
    )
    to_ = StringField(
      'to_',
      validators=[
        DataRequired(message='Please specify a pool destination'),
        Length(min=1, max=32, message='Please specify a valid address'),
      ]
    )
    date = DateField(
      'date',
      validators=[
        DataRequired(message='Please specify a pool date'),
      ]
    )
    time = TimeField(
      'time',
      validators=[
        DataRequired(message='Please specify a pool time'),
      ]
    )
    vehicle = StringField(
      'vehicle',
      validators=[
        DataRequired(message='Please specify a pool vehicle'),
        Length(min=1, max=32, message='Please specify a valid vehicle'),
      ]
    )
    spots = IntegerField(
      'spots',
      validators=[
        DataRequired(message='Please specify the number of pool spots'),
        NumberRange(min=1, max=5, message='Please specify a number between 1 and 5'),
      ]
    )
    submit = SubmitField('Create New Request')
