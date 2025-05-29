import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# Field Selector
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# Year Selector (used for both, but maps exist only for DL)
selected_year = st.slider("Select Year", min_value=2010, max_value=2020, value=2020)

# Map file logic
# if field == "Artificial Intelligence":
#     if selected_year == 2020:
#         map_file = "visualizations/outputs/ai_map_2020.html"
#     else:
#         st.warning(f"⚠️ No AI map available for {selected_year}. Showing 2020 map instead.")
#         map_file = "visualizations/outputs/ai_map_2020.html"
# else:
#     map_file = f"visualizations/outputs/maps_dl_by_year/dl_map_{selected_year}.html"

if field == "Artificial Intelligence":
    map_file = f"visualizations/outputs/maps_ai_by_year/ai_map_{selected_year}.html"
else:
    map_file = f"visualizations/outputs/maps_dl_by_year/dl_map_{selected_year}.html"


# World Map Display
st.subheader(f"🌍 World Map ({selected_year}) - {field}")
try:
    with open(map_file, "r", encoding="utf-8") as f:
        html = f.read()
    st.components.v1.html(html, height=600, scrolling=True)
except FileNotFoundError:
    st.error(f"Map file not found for {selected_year}. Please check data availability.")

# Divider
st.markdown("---")

# Top 5 Growth Chart (2020 only)
growth_img = {
    "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
    "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
}[field]

st.subheader(f"📈 Top 5 Countries by Growth in {field}")
st.image(growth_img, use_container_width=True)

# Divider
st.markdown("---")

# Line Chart for US, CN, DE
st.subheader("📉 Trends in US, China, Germany (AI vs Deep Learning)")
trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
st.image(trend_img, use_container_width=True)

# Divider
st.markdown("---")

# CSV download buttons
st.subheader("📥 Download Raw Data (CSV)")
ai_csv = "data/raw/ai_publication_counts.csv"
dl_csv = "data/raw/deep_learning_publication_counts.csv"

df = pd.read_csv(ai_csv if field == "Artificial Intelligence" else dl_csv)

st.download_button(
    label=f"Download {field} Data as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"{field.lower().replace(' ', '_')}_publication_counts.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
