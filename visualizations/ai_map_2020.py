import folium
import pandas as pd
import requests
import os

# Load AI data
df = pd.read_csv("data/raw/ai_publication_counts.csv")
latest_year = df["year"].max()
df_latest = df[df["year"] == latest_year].copy()

# Extract ISO Alpha-2 from OpenAlex URL
df_latest["alpha_2"] = df_latest["country_code"].apply(lambda x: x.split("/")[-1])

# Map Alpha-2 to Alpha-3 (needed by Folium map)
def alpha2_to_alpha3():
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    response = requests.get(url)
    return {entry["alpha-2"]: entry["alpha-3"] for entry in response.json()}

alpha_map = alpha2_to_alpha3()
df_latest["iso_a3"] = df_latest["alpha_2"].map(alpha_map)
df_latest = df_latest.dropna(subset=["iso_a3"])

# GeoJSON data
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
    legend_name=f"AI Publications in {latest_year}",
).add_to(m)

# Save output
os.makedirs("visualizations/outputs", exist_ok=True)
output_path = "visualizations/outputs/ai_map_2020.html"
m.save(output_path)
print(f"AI world map saved to {output_path}")
