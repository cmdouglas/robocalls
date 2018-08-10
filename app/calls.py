import json
import phonenumbers

from app import app
from app.client import client


def format_phone(phone, format=phonenumbers.PhoneNumberFormat.E164):
    return phonenumbers.format_number(
        phonenumbers.parse(phone, 'US'), format
    )


def make_calls(person, reps):
    # only make one call if the recipient is overridden
    if app.config.get('PHONE_RECIPIENT_OVERRIDE'):
        reps = reps[:1]

    for rep in reps:
        make_call(person, rep)


def make_call(person, rep):
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
        'first_name': person.given_name,
        'last_name': person.family_name,
        'callback_number': format_phone(person.phone_number, phonenumbers.PhoneNumberFormat.NATIONAL),
        'zip': ' '.join(c for c in person.postal_code)
    }

    app.logger.info(f"Placing call from {call_from} to {call_to}", parameters)
    response = client().post(
        f'https://studio.twilio.com/v1/Flows/{flow_sid}/Engagements',
        {
            'To': call_to,
            'From': call_from,
            'Parameters': json.dumps(parameters)
        },
        auth=(account_sid, auth_token)
    )

    response.raise_for_status()
    app.logger.info("Successfully placed call")
