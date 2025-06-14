import pandas as pd
import folium
import os
import requests

def alpha2_to_alpha3_map():
    url = "https://raw.githubusercontent.com/lukes/ISO-3166-Countries-with-Regional-Codes/master/all/all.json"
    resp = requests.get(url)
    return {item["alpha-2"]: item["alpha-3"] for item in resp.json()}

def generate_range_maps(df, label, output_dir):
    df["alpha_2"] = df["country_code"].apply(lambda x: x.split("/")[-1])
    iso_map = alpha2_to_alpha3_map()
    df["iso_a3"] = df["alpha_2"].map(iso_map)
    df = df.dropna(subset=["iso_a3"])

    os.makedirs(output_dir, exist_ok=True)
    geo_url = "https://raw.githubusercontent.com/python-visualization/folium/master/examples/data/world-countries.json"

    for start in range(2010, 2020):
        for end in range(start + 1, 2021):
            df_range = df[(df["year"] >= start) & (df["year"] <= end)]
            agg_df = df_range.groupby("iso_a3")["count"].sum().reset_index()

            m = folium.Map(location=[20, 0], zoom_start=2)
            folium.Choropleth(
                geo_data=geo_url,
                data=agg_df,
                columns=["iso_a3", "count"],
                key_on="feature.id",
                fill_color="YlGnBu",
                fill_opacity=0.7,
                line_opacity=0.2,
                legend_name=f"{label} Publications ({start}–{end})"
            ).add_to(m)

            m.save(f"{output_dir}/{label.lower().replace(' ', '_')}_map_{start}_{end}.html")
            print(f"✅ Saved: {label} {start}–{end}")

# Load datasets
df_ai = pd.read_csv("data/raw/ai_publication_counts.csv")
df_dl = pd.read_csv("data/raw/deep_learning_publication_counts.csv")

generate_range_maps(df_ai, "AI", "visualizations/outputs/maps_ai_by_year_range")
generate_range_maps(df_dl, "Deep Learning", "visualizations/outputs/maps_dl_by_year_range")