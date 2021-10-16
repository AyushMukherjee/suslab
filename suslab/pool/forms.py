from flask_wtf import FlaskForm
from wtforms.fields import StringField, DateField, TimeField
from wtforms.validators import InputRequired, Length


class PoolForm(FlaskForm):
    from_ = StringField(
      'Pool From',
      validators=[
        InputRequired(message='You must provide a pool source'),
        Length(min=1, max=128, message='Length wrong'),
      ]
    )
    to_ = StringField(
      'Pool To',
      validators=[
        InputRequired(message='You must provide a pool destination'),
        Length(min=1, max=128, message='Length wrong'),
      ]
    )
    date = DateField(
      'Pool Date',
      validators=[
        InputRequired(message='You must provide a pool date'),
      ]
    )
    time = TimeField(
      'Pool Time',
      validators=[
        InputRequired(message='You must provide a pool time'),
      ]
    )
