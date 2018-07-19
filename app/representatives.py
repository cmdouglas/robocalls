import json
import requests


def get_reps_by_postal_code(postal_code):
    # TODO: implement some form of caching
    url = f'http://whoismyrepresentative.com/getall_mems.php?zip={postal_code}&output=json'
    response = requests.get(url)
    content = response.content.decode(response.apparent_encoding)
    try:
        content = json.loads(content)
    except json.decoder.JSONDecodeError:
        return []

    return content['results']
