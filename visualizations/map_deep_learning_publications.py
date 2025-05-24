import folium
import pandas as pd
import json
import requests
import os

# Load publication data
df = pd.read_csv("data/raw/deep_learning_publication_counts.csv")

# Get latest year (2020)
latest_year = df["year"].max()
df_latest = df[df["year"] == latest_year].copy()

# Extract alpha-2 country code (e.g., "KR" from "https://openalex.org/countries/KR")
df_latest["alpha_2"] = df_latest["country_code"].apply(lambda x: x.split("/")[-1])

# Map Alpha-2 → Alpha-3
def alpha2_to_alpha3():
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    response = requests.get(url)
    data = response.json()
    mapping = {item["alpha-2"]: item["alpha-3"] for item in data}
    return mapping

alpha_map = alpha2_to_alpha3()
df_latest["iso_a3"] = df_latest["alpha_2"].map(alpha_map)

# Drop any missing iso_a3
df_latest = df_latest.dropna(subset=["iso_a3"])

# Load geojson
geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"

# Create map
m = folium.Map(location=[20, 0], zoom_start=2)

folium.Choropleth(
    geo_data=geo_url,
    name="choropleth",
    data=df_latest,
    columns=["iso_a3", "count"],
    key_on="feature.id",
    fill_color="YlGnBu",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name=f"Deep Learning Publications in {latest_year}",
).add_to(m)

# Save map
os.makedirs("visualizations/outputs", exist_ok=True)
output_path = "visualizations/outputs/deep_learning_map_2020.html"
m.save(output_path)

print(f"Map saved to {output_path}")
