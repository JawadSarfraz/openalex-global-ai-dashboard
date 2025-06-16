import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import folium
import json
import streamlit.components.v1 as components

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.openalex_api import fetch_openalex_data

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# --- Field Selector ---
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# --- Year Range Slider ---
year_range = st.slider("Select Year Range", min_value=2010, max_value=2020, value=(2010, 2020))
year_from, year_to = year_range

# --- Load OpenAlex Data ---
data_load_state = st.text("Loading data from OpenAlex...")
df_live = fetch_openalex_data(field, (year_from, year_to))
data_load_state.text("✓ Live data loaded successfully")

# --- Clean and Format Data ---
if "country_code" in df_live.columns:
    df_live["country_code"] = df_live["country_code"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else x)

def get_country_name(alpha2_code):
    try:
        return pycountry.countries.get(alpha_2=alpha2_code).name
    except:
        return alpha2_code

def alpha2_to_alpha3(alpha2):
    try:
        return pycountry.countries.get(alpha_2=alpha2).alpha_3
    except:
        return None

df_live["country_name"] = df_live["country_code"].apply(get_country_name)
df_live["iso_a3"] = df_live["country_code"].apply(alpha2_to_alpha3)
df_live = df_live.dropna(subset=["iso_a3"])

# --- Calculate Share ---
total_count = df_live["count"].sum()
df_live["share (%)"] = round((df_live["count"] / total_count) * 100, 2)

# --- Display Warning if Empty ---
if df_live.empty:
    st.warning("⚠️ No data available for the selected year range.")
else:
    # --- Choropleth Map with folium ---
    st.subheader(f"🗺️ Choropleth Map of {field} Publications ({year_from}–{year_to})")

    with open("assets/world-countries.json", "r", encoding="utf-8") as f:
        geojson_data = json.load(f)

    m = folium.Map(location=[20, 0], zoom_start=2)
    folium.Choropleth(
        geo_data=geojson_data,
        name="choropleth",
        data=df_live,
        columns=["iso_a3", "count"],
        key_on="feature.id",
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=f"{field} Publications ({year_from}–{year_to})",
    ).add_to(m)

    map_path = "visualizations/outputs/live_map.html"
    m.save(map_path)
    components.html(open(map_path, 'r', encoding='utf-8').read(), height=600, scrolling=True)

    # --- Table Display ---
    st.subheader(f"🌍 Publications by Country ({year_from}–{year_to}) - {field}")
    st.dataframe(
        df_live[["country_name", "count", "share (%)"]]
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )

    # --- Divider ---
    st.markdown("---")

    # --- Growth Chart ---
    growth_img = {
        "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
        "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
    }[field]
    st.subheader(f"📈 Top 5 Countries by Growth in {field} (2010–2020)")
    st.image(growth_img, use_container_width=True)

    # --- Divider ---
    st.markdown("---")

    # --- Line Chart ---
    st.subheader("📉 Trends in US, China, Germany (AI vs Deep Learning)")
    trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
    st.image(trend_img, use_container_width=True)

    # --- Divider ---
    st.markdown("---")

    # --- CSV Download ---
    st.subheader("📥 Download Fetched Data (CSV)")
    st.download_button(
        label=f"Download {field} Data ({year_from}–{year_to}) as CSV",
        data=df_live[["country_name", "count", "share (%)"]].to_csv(index=False).encode('utf-8'),
        file_name=f"{field.lower().replace(' ', '_')}_openalex_{year_from}_{year_to}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
