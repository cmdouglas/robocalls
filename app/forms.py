from phonenumbers import is_possible_number_string

from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, ValidationError

from wtforms.validators import Email, DataRequired, Regexp


class PhoneValidator:
    def __init__(self, region='US', message=None):
        if not message:
            message = "Invalid phone number"

        self.region = region
        self.message = message

    def __call__(self, form, field):
        if not is_possible_number_string(field.data, self.region):
            raise ValidationError(self.message)


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
    phone_number = StringField('Phone Number', validators=[DataRequired(), PhoneValidator()])
    recaptcha = RecaptchaField()
