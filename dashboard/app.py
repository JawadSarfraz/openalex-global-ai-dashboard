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
from services.openalex_api import fetch_openalex_data, fetch_openalex_concepts, fetch_country_citations, fetch_total_publications_by_country

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

# --- Load Total Publications Data for Normalization ---
with st.spinner("Loading total publications data for specialization analysis..."):
    df_total = fetch_total_publications_by_country((year_from, year_to))
data_load_state.text("✓ Live data loaded successfully")

# --- Clean and Format Data ---
if "country_code" in df_live.columns:
    df_live["country_code"] = df_live["country_code"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else x)

# Also clean country codes in df_total
if "country_code" in df_total.columns:
    df_total["country_code"] = df_total["country_code"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else x)

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

# --- Calculate Specialization Ratio FIRST ---
# Merge with total publications data before any other processing
df_live = df_live.merge(df_total, on="country_code", how="left")
df_live["specialization_ratio"] = round((df_live["count"] / df_live["total_publications"]) * 100, 2)
df_live["specialization_ratio"] = df_live["specialization_ratio"].fillna(0)

# --- Now add country names and ISO codes ---
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
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["📊 Publication Counts", "🎯 Specialization Analysis"])
    
    with tab1:
        table_cols = ["country_name", "count", "share (%)", "total_citations"]
        st.dataframe(
            df_live[table_cols]
            .sort_values(by="count", ascending=False)
            .reset_index(drop=True)
        )
        st.info("Citation data is fetched only for the top 5 countries by publication count. Others are not fetched to optimize performance.")
    
    with tab2:
        # Specialization analysis table
        specialization_cols = ["country_name", "count", "total_publications", "specialization_ratio"]
        df_specialization = df_live[specialization_cols].copy()
        df_specialization = df_specialization.sort_values(by="specialization_ratio", ascending=False).reset_index(drop=True)
        
        st.markdown("### 🎯 Research Specialization Analysis")
        st.markdown("**Specialization Ratio** = (Field Publications / Total Publications) × 100")
        st.markdown("This shows which countries are truly specializing in this research field, regardless of their total research volume.")
        
        # Debug info
        st.write(f"Total countries in dataset: {len(df_specialization)}")
        st.write(f"Countries with count > 0: {len(df_specialization[df_specialization['count'] > 0])}")
        st.write(f"Countries with specialization > 0: {len(df_specialization[df_specialization['specialization_ratio'] > 0])}")
        
        st.dataframe(df_specialization)
        
        # Show top 10 specialized countries
        st.markdown("### 🏆 Top 10 Countries by Specialization")
        top_specialized = df_specialization.head(10)
        st.dataframe(top_specialized)
        
        # Create a bar chart for top specialized countries
        fig, ax = plt.subplots(figsize=(12, 6))
        top_specialized_chart = top_specialized.head(10)
        ax.barh(top_specialized_chart["country_name"], top_specialized_chart["specialization_ratio"])
        ax.set_xlabel("Specialization Ratio (%)")
        ax.set_title(f"Top 10 Countries by {field_display} Specialization ({year_from}–{year_to})")
        ax.invert_yaxis()
        plt.tight_layout()
        st.pyplot(fig)

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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.download_button(
            label=f"Download Publication Counts ({year_from}–{year_to})",
            data=df_live[table_cols].to_csv(index=False).encode('utf-8'),
            file_name=f"{field_display.lower().replace(' ', '_')}_publications_{year_from}_{year_to}.csv",
            mime="text/csv"
        )
    
    with col2:
        specialization_export_cols = ["country_name", "count", "total_publications", "specialization_ratio", "share (%)"]
        st.download_button(
            label=f"Download Specialization Analysis ({year_from}–{year_to})",
            data=df_live[specialization_export_cols].to_csv(index=False).encode('utf-8'),
            file_name=f"{field_display.lower().replace(' ', '_')}_specialization_{year_from}_{year_to}.csv",
            mime="text/csv"
        )

    st.markdown("---")
    st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
