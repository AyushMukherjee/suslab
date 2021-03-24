from flask_wtf import FlaskForm
from wtforms.fields import StringField, TextAreaField
from wtforms.validators import InputRequired, Length


class ProductForm(FlaskForm):
    item = StringField('Item Name', validators=[
                        InputRequired(message='You must provide an item name'),
                        Length(min=1, max=128, message='Length wrong'),
                      ])
    description = TextAreaField('Description',
                                validators=[
                                    InputRequired(
                                        message='You must provide an item description'
                                    ),
                                    Length(min=1, max=128, message='Length wrong')
                                ])
