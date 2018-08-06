from app import app
from app.client import client

url = "https://actionnetwork.org/api/v2/people/"
headers = {"OSDI-API-Token": app.config.get('ACTION_NETWORK_KEY')}


def persist_person(person):
    if get_person_by_email(person.email):
        app.logger.info(f"Person: {person.email} already exists.")
        return

    create_person(person)


def get_person_by_email(email):
    app.logger.info(f"Looking up: {email}")

    response = client().get(f"{url}?filter=email eq '{email}'", headers=headers)
    response.raise_for_status()
    search_result = response.json()
    return search_result.get('_embedded', {}).get('osdi:people')


def create_person(person):
    app.logger.info(f"Creating person: {person.email} {person.given_name} {person.family_name} {person.postal_code}")
    json = {
        'person': {
            'family_name': person.family_name,
            'given_name': person.given_name,
            'postal_addresses': [{
                'address_lines': [],
                'locality': '',
                'region': '',
                'country': 'US',
                'postal_code': person.postal_code
            }],
            'email_addresses': [{
                'address': person.email
            }],
            'custom_fields': [],
        },
        'add_tags': ['dialer']
    }
    response = client().post(url, json=json, headers=headers)
    response.raise_for_status()
    app.logger.info(
        f"Successfully created person: {person.email} {person.given_name} {person.family_name} {person.postal_code}"
    )
