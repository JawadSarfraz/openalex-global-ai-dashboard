import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# Field Selector
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# Year Range Selector
year_range = st.slider("Select Year Range", min_value=2010, max_value=2020, value=(2010, 2020))
year_from, year_to = year_range

# Map File Logic
if field == "Artificial Intelligence":
    if year_from == year_to == 2020:
        map_file = "visualizations/outputs/maps_ai_by_year/ai_map_2020.html"
    else:
        st.warning("⚠️ AI maps only available for 2020. Showing 2020 map instead.")
        map_file = "visualizations/outputs/maps_ai_by_year/ai_map_2020.html"
else:
    if os.path.exists(f"visualizations/outputs/maps_dl_by_year/dl_map_{year_to}.html"):
        map_file = f"visualizations/outputs/maps_dl_by_year/dl_map_{year_to}.html"
    else:
        st.warning(f"⚠️ Deep Learning map not available for {year_to}. Showing 2020 map instead.")
        map_file = "visualizations/outputs/maps_dl_by_year/dl_map_2020.html"

# World Map Display
st.subheader(f"🌍 World Map (Latest: {year_to}) - {field}")
try:
    with open(map_file, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600, scrolling=True)
except FileNotFoundError:
    st.error("❌ Map file not found. Please verify data and path.")

# Divider
st.markdown("---")

# Top 5 Growth Chart
growth_img = {
    "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
    "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
}[field]

st.subheader(f"📈 Top 5 Countries by Growth in {field} (2010–2020)")
st.image(growth_img, use_container_width=True)

# Divider
st.markdown("---")

# Line Chart
st.subheader("📉 Trends in US, China, Germany (AI vs Deep Learning)")
trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
st.image(trend_img, use_container_width=True)

# Divider
st.markdown("---")

# CSV Download
st.subheader("📥 Download Filtered Data (CSV)")
ai_csv = "data/raw/ai_publication_counts.csv"
dl_csv = "data/raw/deep_learning_publication_counts.csv"

df_raw = pd.read_csv(ai_csv if field == "Artificial Intelligence" else dl_csv)
df_filtered = df_raw[(df_raw["year"] >= year_from) & (df_raw["year"] <= year_to)]

st.download_button(
    label=f"Download {field} Data ({year_from}–{year_to}) as CSV",
    data=df_filtered.to_csv(index=False).encode('utf-8'),
    file_name=f"{field.lower().replace(' ', '_')}_data_{year_from}_{year_to}.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
