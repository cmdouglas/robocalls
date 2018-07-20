import requests
from requests.adapters import HTTPAdapter
from urllib3 import Retry
from urllib.parse import quote


def requests_retry_session(
        app,
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


class ActionNetworkApi:
    """Python wrapper for Action Network API."""

    def __init__(self, app, **kwargs):
        """Instantiate the API client and get config."""
        self.app = app
        self.headers = {"OSDI-API-Token": app.config.get('ACTIONNETWORK_KEY')}
        self.refresh_config()
        self.base_url = self.config.get('links', {}).get('self', 'https://actionnetwork.org/api/v2/')
        print(self.config['motd'])

    def refresh_config(self):
        """Get a new version of the base_url config."""
        self.config = requests_retry_session(self.app).get(url="https://actionnetwork.org/api/v2/",
                                                   headers=self.headers).json()

    def resource_to_url(self, resource):
        """Convert a named endpoint into a URL.
        Args:
            resource (str):
                resource name (e.g. 'links', 'people', etc.)
        Returns:
            (str) Full resource endpoint URL.
        """
        if resource in self.config.get('_links', {}).keys():
            return self.config['_links'][resource]['href']
        try:
            return self.config['_links']["osdi:{0}".format(resource)]['href']
        except KeyError:
            raise KeyError("Unknown Resource %s", resource)

    def get_resource(self, resource):
        """Get a resource endpoint by name.
        Args:
            resource (str):
                Resource endpoint of the format 'people', 'events', 'lists', etc.
        Returns:
            (dict) API response from endpoint or `None` if not found/valid.
        """
        url = self.resource_to_url(resource)
        return requests_retry_session(self.app).get(url, headers=self.headers).json()

    def get_person(self, person_id=None, search_by='email', search_string=None):
        """Search for a user.
        Args:
            person_id:
                Action network person id
            search_by (str):
                Field by which to search for a user. 'email' is the default.
            search_string (str):
                String to search for within the field given by `search_by`
        Returns:
            (dict) person json if found, otherwise `None`
        """
        if person_id:
            url = "{0}people/{1}".format(self.base_url, person_id)
        else:
            url = "{0}people/?filter={1} eq '{2}'".format(
                self.base_url,
                search_by,
                quote(search_string))

        resp = requests_retry_session(self.app).get(url, headers=self.headers)
        return resp.json()

    def create_person(self,
                      email=None,
                      given_name='',
                      family_name='',
                      address=list(),
                      city='',
                      state='',
                      country='',
                      postal_code='',
                      tags=list(),
                      custom_fields=None):
        """Create a user.
        Documentation here: https://actionnetwork.org/docs/v2/person_signup_helper
        Args:
            email ((str, list)):
                email address (or, if list, addresses) of the person
            given_name (str, optional):
                first name of the person
            family_name (str, optional):
                last name of the person
            address ((str, list), optional):
                address of the person. if a str, then one address line
                only. if a list, then address_lines in action network
                will be respected (for apartments or companies etc.)
            city (str, optional):
                city of the person.
            state (str, optional):
                state of the person
            country (str, optional):
                country code for the person.
            postal_code (str, optional):
                postal or zip code of the person.
            tags ((str, list), optional):
                add any tags you want when creating a person.
            custom_fields (dict, optional):
                dict of custom fields to pass to the api
        Returns:
            (dict) A fully fleshed out dictionary representing a person,
            containing the above attributes and additional attributes
            set by Action Network.
        """
        if not custom_fields:
            custom_fields = {}

        url = "{0}people/".format(self.base_url)
        payload = {
            'person': {
                'family_name': family_name,
                'given_name': given_name,
                'postal_addresses': [{
                    'address_lines': list(address),
                    'locality': city,
                    'region': state,
                    'country': country,
                    'postal_code': postal_code
                }],
                'email_addresses': [{
                    'address': email
                }],
                'custom_fields': custom_fields,
            },
            'add_tags': list(tags)
        }

        resp = requests_retry_session(self.app).post(url, json=payload, headers=self.headers)
        return resp.json()

    def update_person(self,
                      person_id=None,
                      email=None,
                      given_name=None,
                      family_name=None,
                      address=list(),
                      city=None,
                      state=None,
                      country=None,
                      postal_code=None,
                      tags=list(),
                      custom_fields=None):
        """Update a user.
        Args:
            email ((str, list)):
                email address (or, if list, addresses) of the person
            given_name (str, optional):
                first name of the person
            family_name (str, optional):
                last name of the person
            address ((str, list), optional):
                address of the person. if a str, then one address line
                only. if a list, then address_lines in action network
                will be respected (for apartments or companies etc.)
            city (str, optional):
                city of the person.
            country (str, optional):
                country code for the person.
            postal_code (str, optional):
                postal or zip code of the person.
            tags ((str, list), optional):
                add any tags you want when creating a person.
            custom_fields (dict, optional):
                dict of custom fields to pass to the api
        Returns:
            (dict) A fully fleshed out dictionary representing a person, containing the above
            attributes and additional attributes set by Action Network.
        """
        if not custom_fields:
            custom_fields = {}

        url = "{0}people/{1}".format(self.base_url, person_id)
        payload = {
            'family_name': family_name,
            'given_name': given_name,
            'postal_addresses': [{
                'address_lines': list(address),
                'locality': city,
                'region': state,
                'country': country,
                'postal_code': postal_code
            }],
            'email_addresses': [{
                'address': email
            }],
            'add_tags': list(tags),
            'custom_fields': custom_fields,
        }

        resp = requests_retry_session(self.app).put(url, json=payload, headers=self.headers)
        return resp.json()
