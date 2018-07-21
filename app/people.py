import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry

from app import app

url = "https://actionnetwork.org/api/v2/people/"
headers = {"OSDI-API-Token": app.config.get('ACTION_NETWORK_KEY')}


def requests_retry_session(
        retries=3,
        backoff_factor=0.3,
        status_forcelist=(500, 502, 504),
        session=None,
):
    session = session or requests.Session()
    session.verify = bool(int(app.config.get('REQUESTS_VERIFY')))

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def get_person_by_email(email):
    response = requests_retry_session().get(f"{url}?filter=email eq '{email}'", headers=headers)
    response.raise_for_status()
    search_result = response.json()
    return search_result.get('_embedded', {}).get('osdi:people')


def create_person(email, given_name='', family_name='', postal_code=''):
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
        'add_tags': []
    }
    return requests_retry_session().post(url, json=person, headers=headers).raise_for_status()
