import json
from werkzeug.contrib.cache import FileSystemCache

from app.client import client


def get_reps_by_postal_code(postal_code):
    cache = FileSystemCache('cache')
    if cache.has(postal_code):
        return cache.get(postal_code)

    url = f'http://whoismyrepresentative.com/getall_mems.php?zip={postal_code}&output=json'
    response = client().get(url)
    content = response.content.decode(response.apparent_encoding)
    try:
        content = json.loads(content)
    except json.decoder.JSONDecodeError:
        content = {'results':[]}

    cache.set(postal_code, content['results'])
    return content['results']
