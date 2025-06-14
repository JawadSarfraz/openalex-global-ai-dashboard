import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
from services.openalex_api import fetch_openalex_data

st.set_page_config(layout="wide")
st.title("\U0001F4CA Global Research Dashboard: AI & Deep Learning (2010–2020)")

# Field Selector
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# Year Range Selector
year_range = st.slider("Select Year Range", min_value=2010, max_value=2020, value=(2010, 2020))
year_from, year_to = year_range

# Fetch OpenAlex live data
data_load_state = st.text("Loading data from OpenAlex...")
df_live = fetch_openalex_data(field, (year_from, year_to))
data_load_state.text("✓ Live data loaded successfully")

# Show World Map (Placeholder for dynamic map - could be folium integration later)
st.subheader(f"\U0001F30D Publications by Country ({year_from}–{year_to}) - {field}")
st.dataframe(df_live.sort_values(by="count", ascending=False).reset_index(drop=True))

# Divider
st.markdown("---")

# Top 5 Growth Chart (Static image for now)
growth_img = {
    "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
    "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
}[field]

st.subheader(f"\U0001F4C8 Top 5 Countries by Growth in {field} (2010–2020)")
st.image(growth_img, use_container_width=True)

# Divider
st.markdown("---")

# Line Chart (Static for now)
st.subheader("\U0001F4C9 Trends in US, China, Germany (AI vs Deep Learning)")
trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
st.image(trend_img, use_container_width=True)

# Divider
st.markdown("---")

# CSV Download
st.subheader("\U0001F4E5 Download Fetched Data (CSV)")

st.download_button(
    label=f"Download {field} Data ({year_from}–{year_to}) as CSV",
    data=df_live.to_csv(index=False).encode('utf-8'),
    file_name=f"{field.lower().replace(' ', '_')}_openalex_{year_from}_{year_to}.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")