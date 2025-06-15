# services/openalex_api.py

import requests
import pandas as pd
from urllib.parse import quote

def fetch_openalex_data(field, year_range):
    """
    Fetches publication counts per country from OpenAlex API for a given field and year range.

    Args:
        field (str): Either "Artificial Intelligence" or "Deep Learning"
        year_range (tuple): (start_year, end_year)

    Returns:
        pd.DataFrame: DataFrame with country-wise publication counts.
    """
    start_year, end_year = year_range

    # Build OpenAlex search query
    query = quote(field)
    url = f"https://api.openalex.org/works?filter=concepts.display_name.search:{query},from_publication_date:{start_year}-01-01,to_publication_date:{end_year}-12-31&group_by=authorships.institutions.country_code&per-page=200"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"OpenAlex API error: {response.status_code}")

    results = response.json().get("group_by", [])

    # Prepare DataFrame
    records = []
    for item in results:
        country_code = item.get("key")
        count = item.get("count", 0)
        records.append({"country_code": country_code, "count": count})

    df = pd.DataFrame(records)
    return df