import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# Selection
field = st.selectbox("Select Field of Research", ["Artificial Intelligence", "Deep Learning"])

# Map
map_file = {
    "Artificial Intelligence": "visualizations/outputs/ai_map_2020.html",
    "Deep Learning": "visualizations/outputs/deep_learning_map_2020.html"
}[field]

st.subheader(f"🌍 World Map (2020) - {field}")
with open(map_file, "r", encoding="utf-8") as f:
    html = f.read()
st.components.v1.html(html, height=600, scrolling=True)

# Top 5 Chart
growth_img = {
    "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
    "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
}[field]

st.subheader(f"📈 Top 5 Countries by Growth in {field}")
st.image(growth_img, use_column_width=True)

# Line Chart (Static — both fields)
st.subheader("📉 Trends in US, China, Germany (AI vs Deep Learning)")
trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
st.image(trend_img, use_column_width=True)

# Optional download
st.markdown("---")
st.caption("Developed for research thesis on global scientific productivity (2010–2020)")
