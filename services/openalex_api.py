# services/openalex_api.py

import requests
import pandas as pd
from urllib.parse import quote

def fetch_openalex_data(concept_id, year_range):
    year_from, year_to = year_range

    # Construct OpenAlex API URL
    base_url = "https://api.openalex.org/works"
    filter_query = f"concepts.id:{concept_id},from_publication_date:{year_from}-01-01,to_publication_date:{year_to}-12-31"
    group_by = "group_by=institutions.country_code"

    params = {
        "filter": filter_query,
        "group_by": "institutions.country_code",
        "mailto": "jawadsarfraz96@gmail.com"  # real email!
    }

    headers = {
        "User-Agent": "OpenAlex Dashboard (mailto:jawadsarfraz96@gmail.com)"
    }

    response = requests.get(base_url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"OpenAlex API error: {response.status_code}")

    items = response.json().get("group_by", [])
    records = [{"country_code": item["key"], "count": item["count"]} for item in items]

    return pd.DataFrame(records)

def fetch_openalex_concepts(per_page=50, max_pages=5):
    """
    Fetch a list of available research fields (concepts) from OpenAlex.
    Returns a list of dicts: [{"id": ..., "display_name": ...}, ...]
    """
    base_url = "https://api.openalex.org/concepts"
    params = {
        "per-page": per_page,
        "mailto": "jawadsarfraz96@gmail.com"
    }
    headers = {
        "User-Agent": "OpenAlex Dashboard (mailto:jawadsarfraz96@gmail.com)"
    }
    concepts = []
    for page in range(1, max_pages + 1):
        params["page"] = page
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            break
        results = response.json().get("results", [])
        if not results:
            break
        for c in results:
            concepts.append({
                "id": c["id"],
                "display_name": c["display_name"]
            })
    return concepts
