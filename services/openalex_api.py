import requests
import pandas as pd
from urllib.parse import quote

# Mapping for field → OpenAlex concept IDs
FIELD_TO_CONCEPT = {
    "Artificial Intelligence": "C41008148",   # OpenAlex ID for AI
    "Deep Learning": "C2778407487",           # OpenAlex ID for DL
}

def fetch_openalex_data(field: str, year_range: tuple):
    """
    Fetch OpenAlex data for a given field and year range.

    Args:
        field (str): Either "Artificial Intelligence" or "Deep Learning".
        year_range (tuple): (start_year, end_year)

    Returns:
        DataFrame: Country-wise publication counts.
    """
    concept_id = FIELD_TO_CONCEPT.get(field)
    year_from, year_to = year_range

    url = (
        f"https://api.openalex.org/works?filter="
        f"concepts.id:{concept_id},"
        f"from_publication_date:{year_from}-01-01,"
        f"to_publication_date:{year_to}-12-31"
        f"&group_by=institutions.country_code"
        f"&mailto=your-email@example.com"
    )

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data: {response.status_code} - {response.text}")

    results = response.json().get("group_by", [])
    rows = []
    for item in results:
        country_code = item.get("key", None)
        count = item.get("count", 0)
        if country_code:
            rows.append({"country_code": country_code, "count": count})

    return pd.DataFrame(rows)