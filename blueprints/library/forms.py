from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import DataRequired, Length


class ProductForm(FlaskForm):
    item = StringField(
        'item',
        validators=[
            DataRequired(message='Please specify an item name'),
            Length(min=1, max=128, message='Length wrong'),
        ]
    )
    description = TextAreaField(
        'description',
        validators=[
            DataRequired(message='Please specify an item description'),
            Length(min=1, max=128, message='Length wrong')
        ]
    )
