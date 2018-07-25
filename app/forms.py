from flask_wtf import FlaskForm
from wtforms import StringField

from wtforms.validators import Email, DataRequired, Regexp


class MakeCallForm(FlaskForm):
    given_name = StringField('Given Name', validators=[DataRequired()])
    family_name = StringField('Family Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    postal_code = StringField(
        'Postal Code',
        validators=[
            DataRequired(),
            Regexp('[0-9]{5}', message="Invalid zip code.")
        ]
    )
