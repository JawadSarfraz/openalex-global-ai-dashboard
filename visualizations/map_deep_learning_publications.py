import folium
import pandas as pd
import json
import requests
import os

# Load publication data
df = pd.read_csv("data/raw/deep_learning_publication_counts.csv")

# Get most recent year for map (e.g., 2020)
latest_year = df["year"].max()
df_latest = df[df["year"] == latest_year]

# Standardize country codes (ISO3)
def alpha2_to_alpha3():
    # Use ISO conversion JSON from public repo (or load locally)
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    response = requests.get(url)
    country_map = {}
    for country in response.json():
        country_map[country["alpha-2"]] = country["alpha-3"]
    return country_map

alpha2_3 = alpha2_to_alpha3()
df_latest["iso_a3"] = df_latest["country_code"].map(alpha2_3)

# Remove missing country codes
df_latest = df_latest.dropna(subset=["iso_a3"])

# Load GeoJSON file for countries
world_geo = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"

# Create Folium Map
m = folium.Map(location=[20, 0], zoom_start=2)

folium.Choropleth(
    geo_data=world_geo,
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
output_file = "visualizations/outputs/deep_learning_map_2020.html"
m.save(output_file)

print(f"Map saved to {output_file}")
