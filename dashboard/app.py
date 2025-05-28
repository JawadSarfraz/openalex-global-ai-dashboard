import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# Field Selector
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# Map HTML path
map_file = {
    "Artificial Intelligence": "visualizations/outputs/ai_map_2020.html",
    "Deep Learning": "visualizations/outputs/deep_learning_map_2020.html"
}[field]

# World Map Display
st.subheader(f"🌍 World Map (2020) - {field}")
with open(map_file, "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=600, scrolling=True)

# Divider
st.markdown("---")

# Top 5 Growth Chart
growth_img = {
    "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
    "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
}[field]

st.subheader(f"📈 Top 5 Countries by Growth in {field}")
st.image(growth_img, use_container_width=True)  # ✅ Updated from use_column_width

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

if field == "Artificial Intelligence":
    df = pd.read_csv(ai_csv)
else:
    df = pd.read_csv(dl_csv)

st.download_button(
    label=f"Download {field} Data as CSV",
    data=df.to_csv(index=False).encode('utf-8'),
    file_name=f"{field.lower().replace(' ', '_')}_publication_counts.csv",
    mime="text/csv"
)

st.markdown("---")
st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
