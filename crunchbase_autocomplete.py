import json
import os

import requests


def find_company(name):
    # TODO: add error handling
    r = requests.get("https://api.crunchbase.com/api/v4/autocompletes",
                     params={"user_key": os.environ.get('CRUNCHBASE_KEY'),
                             "collection_ids": "organization.companies",
                             "query": name})
    result = json.loads(r.text)
    return result


c = find_company("airbnb")
p = json.dumps(c, indent=4, sort_keys=True)
print(p)
