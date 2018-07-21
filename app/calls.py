import phonenumbers
import requests
import json
from flask import flash

from app import app


def format_phone(phone):
    return phonenumbers.format_number(
        phonenumbers.parse(phone, 'US'), phonenumbers.PhoneNumberFormat.E164
    )


def make_calls(given_name, family_name, postal_code, reps):
    # only make one call if the recipient is overridden
    if app.config.get('PHONE_RECIPIENT_OVERRIDE'):
        reps = reps[:1]

    for rep in reps:
        make_call(given_name, family_name, postal_code, rep)
        flash(f'Call placed to <strong>{rep["name"]}</strong> at <strong>{rep["phone"]}</strong>.')


def make_call(given_name, family_name, postal_code, rep):
    account_sid = app.config.get('TWILIO_ACCOUNT_SID')
    auth_token = app.config.get('TWILIO_SECRET')

    recipient_override = app.config.get('PHONE_RECIPIENT_OVERRIDE')

    if recipient_override:
        call_to = format_phone(recipient_override)
    else:
        call_to = format_phone(rep['phone'])

    call_from = app.config.get('TWILIO_NUMBER')

    flow_sid = app.config.get('TWILIO_FLOW_SID')

    contact_name = rep['name']

    parameters = {
        'contact_name': contact_name,
        'first_name': given_name,
        'last_name': family_name,
        'zip': postal_code
    }

    response = requests.post(
        f'https://studio.twilio.com/v1/Flows/{flow_sid}/Engagements',
        {
            'To': call_to,
            'From': call_from,
            'Parameters': json.dumps(parameters)
        },
        auth=(account_sid, auth_token)
    )

    response.raise_for_status()
