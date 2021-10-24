from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TimeField
from wtforms.fields.simple import SubmitField
from wtforms.validators import InputRequired, Length


class PoolForm(FlaskForm):
    from_ = StringField(
      'from_',
      validators=[
        InputRequired(message='Please provide a pool source'),
        Length(min=1, max=128, message='Please provide a valid source'),
      ]
    )
    to_ = StringField(
      'to_',
      validators=[
        InputRequired(message='Please provide a pool destination'),
        Length(min=1, max=128, message='Please provide a valid address'),
      ]
    )
    date = DateField(
      'date',
      validators=[
        InputRequired(message='Please provide a pool date'),
      ]
    )
    time = TimeField(
      'time',
      validators=[
        InputRequired(message='Please provide a pool time'),
      ]
    )
    submit = SubmitField('Create New Request')
