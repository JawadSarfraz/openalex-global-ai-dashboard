import pandas as pd
import folium
import requests
import os

# --- SETTINGS ---
YEAR_FROM = 2015
YEAR_TO = 2018
INPUT_CSV = "data/raw/deep_learning_publication_counts.csv"
OUTPUT_PATH = f"visualizations/outputs/aggregated_dl_map_{YEAR_FROM}_{YEAR_TO}.html"

# Load data
df = pd.read_csv(INPUT_CSV)

# Extract Alpha-2 country codes
df["alpha_2"] = df["country_code"].apply(lambda x: x.split("/")[-1])

# Convert Alpha-2 to Alpha-3 codes
def alpha2_to_alpha3():
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    res = requests.get(url)
    return {entry["alpha-2"]: entry["alpha-3"] for entry in res.json()}

iso_map = alpha2_to_alpha3()
df["iso_a3"] = df["alpha_2"].map(iso_map)
df = df.dropna(subset=["iso_a3"])

# Filter by year range
df_range = df[(df["year"] >= YEAR_FROM) & (df["year"] <= YEAR_TO)]

# Aggregate by iso_a3
df_agg = df_range.groupby("iso_a3")["count"].sum().reset_index()

# Load GeoJSON
geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"

# Generate map
m = folium.Map(location=[20, 0], zoom_start=2)
folium.Choropleth(
    geo_data=geo_url,
    name="choropleth",
    data=df_agg,
    columns=["iso_a3", "count"],
    key_on="feature.id",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"DL Publications ({YEAR_FROM}–{YEAR_TO})"
).add_to(m)

# Save output
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
m.save(OUTPUT_PATH)
print(f"✅ Aggregated map saved to: {OUTPUT_PATH}")