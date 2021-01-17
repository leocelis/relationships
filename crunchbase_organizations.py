import json
import os

import pandas as pd
import requests
from pandas.io.json import json_normalize

userkey = {"user_key": os.environ.get('CRUNCHBASE_KEY')}

query = {
    "field_ids": [
        "identifier",
        "location_identifiers",
        "short_description",
        "categories",
        "num_employees_enum",
        "revenue_range",
        "operating_status",
        "website",
        "linkedin"
    ], "limit": 10,
    "query": [
        {
            "type": "predicate",
            "field_id": "location_identifiers",
            "operator_id": "includes",
            "values": [
                "4ce61f42-f6c4-e7ec-798d-44813b58856b"  # UUID FOR LOS ANGELES
            ]
        },
        {
            "type": "predicate",
            "field_id": "facet_ids",
            "operator_id": "includes",
            "values": [
                "company"
            ]
        }
    ]
}


def company_count(query):
    # TODO: add error handling
    r = requests.post("https://api.crunchbase.com/api/v4/searches/organizations",
                      params=userkey,
                      json=query)
    result = json.loads(r.text)
    total_companies = result["count"]
    return total_companies


def url_extraction(query):
    global raw
    r = requests.post("https://api.crunchbase.com/api/v4/searches/organizations", params=userkey, json=query)
    result = json.loads(r.text)
    normalized_raw = json_normalize(result['entities'])
    raw = raw.append(normalized_raw, ignore_index=True)


raw = pd.DataFrame()
comp_count = company_count(query)
data_acq = 0

# data_acq
while data_acq < comp_count:
    if data_acq != 0:
        last_uuid = raw.uuid[len(raw.uuid) - 1]
        query["after_id"] = last_uuid
        url_extraction(query)
        data_acq = len(raw.uuid)
    else:
        if "after_id" in query:
            query = query.pop("after_id")
            url_extraction(query)
            data_acq = len(raw.uuid)
        else:
            url_extraction(query)
            data_acq = len(raw.uuid)

revenue_range = {
    "r_00000000": "Less than $1M",
    "r_00001000": "$1M to $10M",
    "r_00010000": "$10M to $50M",
    "r_00050000": "$50M to $100M",
    "r_00100000": "$100M to $500M",
    "r_00500000": "$500M to $1B",
    "r_01000000": "$1B to $10B",
    "r_10000000": "$10B+"}

employee_range = {
    "c_00001_00010": "1-10",
    "c_00011_00050": "11-50",
    "c_00051_00100": "51-100",
    "c_00101_00250": "101-250",
    "c_00251_00500": "251-500",
    "c_00501_01000": "501-1000",
    "c_01001_05000": "1001-5000",
    "c_05001_10000": "5001-10000",
    "c_10001_max": "10001+"}

master = pd.DataFrame()
master["uuid"] = raw["uuid"]
master["company"] = raw["properties.identifier.value"]
master["description"] = raw["properties.short_description"]
master["categories"] = raw["properties.categories"].apply(
    lambda x: list(map(itemgetter('value'), x) if isinstance(x, list) else ["Not found"])).apply(
    lambda x: ",".join(map(str, x)))
master["location"] = raw["properties.location_identifiers"].apply(
    lambda x: list(map(itemgetter('value'), x) if isinstance(x, list) else ["Not found"])).apply(
    lambda x: ",".join(map(str, x)))
master["revenue"] = raw["properties.revenue_range"].map(revenue_range)
master["num_of_employees"] = raw["properties.num_employees_enum"].map(employee_range)
# master["rank"] = raw["properties.rank_org_company"]
master["linkedin"] = raw["properties.linkedin.value"]
master["website"] = raw["properties.website.value"]
master["status"] = raw["properties.operating_status"]
master = master.fillna("NA")

print(master)
