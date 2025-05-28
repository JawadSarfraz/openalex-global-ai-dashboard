import pandas as pd
import folium
import requests
import os

df = pd.read_csv("data/raw/deep_learning_publication_counts.csv")
years = sorted(df["year"].unique())

# Extract Alpha-2
df["alpha_2"] = df["country_code"].apply(lambda x: x.split("/")[-1])

# Convert to Alpha-3
def alpha2_to_alpha3():
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    res = requests.get(url)
    return {r["alpha-2"]: r["alpha-3"] for r in res.json()}

iso_map = alpha2_to_alpha3()
df["iso_a3"] = df["alpha_2"].map(iso_map)
df = df.dropna(subset=["iso_a3"])

# GeoJSON
geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"
os.makedirs("visualizations/outputs/maps_dl_by_year", exist_ok=True)

for year in years:
    df_year = df[df["year"] == year]

    m = folium.Map(location=[20, 0], zoom_start=2)
    folium.Choropleth(
        geo_data=geo_url,
        name="choropleth",
        data=df_year,
        columns=["iso_a3", "count"],
        key_on="feature.id",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"DL Publications in {year}",
    ).add_to(m)

    m.save(f"visualizations/outputs/maps_dl_by_year/dl_map_{year}.html")
    print(f"Saved map for {year}")
