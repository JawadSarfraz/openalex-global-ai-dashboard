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
from services.openalex_api import fetch_openalex_data, fetch_openalex_concepts, fetch_country_citations

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# --- Dynamic Field Selector ---
with st.spinner("Fetching available research fields from OpenAlex..."):
    concepts = fetch_openalex_concepts(per_page=50, max_pages=5)
    concept_options = {c["display_name"]: c["id"] for c in concepts}
field_display = st.selectbox("Select Field of Research", list(concept_options.keys()))
selected_concept_id = concept_options[field_display]

# --- Year Range Slider ---
year_range = st.slider("Select Year Range", min_value=2010, max_value=2020, value=(2010, 2020))
year_from, year_to = year_range

# --- Load OpenAlex Data ---
data_load_state = st.text("Loading data from OpenAlex...")
df_live = fetch_openalex_data(selected_concept_id, (year_from, year_to))
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

# --- Fetch Citation Data for Top 5 Countries Only ---
df_live_sorted = df_live.sort_values(by="count", ascending=False).reset_index(drop=True)
top5_countries = df_live_sorted.head(5)["country_code"].tolist()
citation_data = {}
with st.spinner("Fetching citation data for top 5 countries (may take a few seconds)..."):
    for country_code in top5_countries:
        citations = fetch_country_citations(selected_concept_id, country_code, (year_from, year_to))
        citation_data[country_code] = citations
# Set citation data for top 5, None for others
df_live["total_citations"] = df_live["country_code"].apply(lambda x: citation_data.get(x, None))

# --- Citation Data ---
if df_live["total_citations"].notnull().any():
    total_citations = df_live["total_citations"].sum()
    avg_citations = (df_live["total_citations"] / df_live["count"]).mean()
else:
    total_citations = None
    avg_citations = None

# --- Display Warning if Empty ---
if df_live.empty:
    st.warning("⚠️ No data available for the selected year range.")
else:
    # --- Choropleth Map with folium ---
    st.subheader(f"🗺️ Choropleth Map of {field_display} Publications ({year_from}–{year_to})")

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
        legend_name=f"{field_display} Publications ({year_from}–{year_to})",
    ).add_to(m)

    map_path = "visualizations/outputs/live_map.html"
    m.save(map_path)
    components.html(open(map_path, 'r', encoding='utf-8').read(), height=600, scrolling=True)

    # --- Citation Summary ---
    if total_citations is not None:
        st.metric("Total Citations (all countries)", int(total_citations))
        st.metric("Average Citations per Publication", f"{avg_citations:.2f}")

    # --- Table Display ---
    st.subheader(f"🌍 Publications by Country ({year_from}–{year_to}) - {field_display}")
    table_cols = ["country_name", "count", "share (%)", "total_citations"]
    st.dataframe(
        df_live[table_cols]
        .sort_values(by="count", ascending=False)
        .reset_index(drop=True)
    )
    st.info("Citation data is fetched only for the top 5 countries by publication count. Others are not fetched to optimize performance.")

    # --- Divider ---
    st.markdown("---")

    # --- Growth Chart ---
    st.subheader(f"📈 Top 5 Countries by Growth in {field_display} (2010–2020)")
    st.info("Growth chart is only available for AI and Deep Learning at the moment.")

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
        label=f"Download {field_display} Data ({year_from}–{year_to}) as CSV",
        data=df_live[table_cols].to_csv(index=False).encode('utf-8'),
        file_name=f"{field_display.lower().replace(' ', '_')}_openalex_{year_from}_{year_to}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
