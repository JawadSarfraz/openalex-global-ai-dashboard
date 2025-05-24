import requests
import pandas as pd
from tqdm import tqdm
import os

CONCEPT_ID = "C108583219"  # Deep Learning
YEARS = list(range(2010, 2021))
FIELDS = "works_count,group_key"
OUTPUT_PATH = "data/raw/deep_learning_publication_counts.csv"

os.makedirs("data/raw", exist_ok=True)

def fetch_counts_by_country(concept_id, year):
    url = (
        f"https://api.openalex.org/works"
        f"?filter=concepts.id:{concept_id},publication_year:{year}"
        f"&group_by=authorships.institutions.country_code"
    )
    response = requests.get(url)
    response.raise_for_status()
    return response.json()["group_by"]

def main():
    all_data = []

    for year in tqdm(YEARS, desc="Fetching year-wise data"):
        try:
            year_data = fetch_counts_by_country(CONCEPT_ID, year)
            for entry in year_data:
                all_data.append({
                    "year": year,
                    "country_code": entry["key"],
                    "count": entry["count"]
                })
        except Exception as e:
            print(f"Failed to fetch data for {year}: {e}")

    df = pd.DataFrame(all_data)
    df.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
