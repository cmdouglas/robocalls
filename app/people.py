import logging
from app import app
from app.client import client

url = "https://actionnetwork.org/api/v2/people/"
headers = {"OSDI-API-Token": app.config.get('ACTION_NETWORK_KEY')}


def persist_person(email, given_name='', family_name='', postal_code=''):
    if get_person_by_email(email):
        logging.info(f"Person: {email} already exists.")
        return

    create_person(email, given_name, family_name, postal_code)


def get_person_by_email(email):
    logging.info(f"Looking up: {email} already exists.")

    response = client().get(f"{url}?filter=email eq '{email}'", headers=headers)
    response.raise_for_status()
    search_result = response.json()
    return search_result.get('_embedded', {}).get('osdi:people')


def create_person(email, given_name='', family_name='', postal_code=''):
    logging.info(f"Creating person: {email} {given_name} {family_name} {postal_code}")
    person = {
        'person': {
            'family_name': family_name,
            'given_name': given_name,
            'postal_addresses': [{
                'address_lines': [],
                'locality': '',
                'region': '',
                'country': 'US',
                'postal_code': postal_code
            }],
            'email_addresses': [{
                'address': email
            }],
            'custom_fields': [],
        },
        'add_tags': ['dialer']
    }
    response = client().post(url, json=person, headers=headers)
    logging.info(f"Successfully created person: {email} {given_name} {family_name} {postal_code}")
    response.raise_for_status()
