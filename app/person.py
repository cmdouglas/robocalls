from pyactionnetwork import ActionNetworkApi


def persist_user(app, email, given_name='', family_name='', postal_code=''):
    return
    api = ActionNetworkApi(app.config.get('ACTION_NETWORK_KEY'))

    if api.get_person(search_string=email):
        return

    api.create_person(email, given_name=given_name, family_name=family_name, postal_code=postal_code)
