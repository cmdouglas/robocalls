from app.actionnetwork import ActionNetworkApi


def persist_person(app, email, given_name='', family_name='', postal_code=''):
    api = ActionNetworkApi(app)

    if api.get_person(search_string=email):
        return

    api.create_person(email, given_name=given_name, family_name=family_name, postal_code=postal_code)
