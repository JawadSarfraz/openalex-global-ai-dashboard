import sys
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os
import pycountry

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

# Clean up country codes (e.g., from 'https://openalex.org/geo/country:DE' to 'DE')
if "country_code" in df_live.columns:
    df_live["country_code"] = df_live["country_code"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else x)

# Map readable country names
def get_country_name(alpha2_code):
    try:
        return pycountry.countries.get(alpha_2=alpha2_code).name
    except:
        return alpha2_code  # fallback if not found

df_live["country_name"] = df_live["country_code"].apply(get_country_name)

# Handle empty API response
if df_live.empty:
    st.warning("⚠️ No data available for the selected year range.")
else:
    # Show World Map (placeholder for now)
    st.subheader(f"\U0001F30D Publications by Country ({year_from}–{year_to}) - {field}")
    st.dataframe(df_live[["country_name", "count"]].sort_values(by="count", ascending=False).reset_index(drop=True))

    # Divider
    st.markdown("---")

    # Top 5 Growth Chart (static)
    growth_img = {
        "Artificial Intelligence": "visualizations/outputs/top5_growth_ai.png",
        "Deep Learning": "visualizations/outputs/top5_growth_dl.png"
    }[field]

    st.subheader(f"\U0001F4C8 Top 5 Countries by Growth in {field} (2010–2020)")
    st.image(growth_img, use_container_width=True)

    # Divider
    st.markdown("---")

    # Line Chart (static)
    st.subheader("\U0001F4C9 Trends in US, China, Germany (AI vs Deep Learning)")
    trend_img = "visualizations/outputs/line_trend_us_cn_de.png"
    st.image(trend_img, use_container_width=True)

    # Divider
    st.markdown("---")

    # CSV Download
    st.subheader("\U0001F4E5 Download Fetched Data (CSV)")
    st.download_button(
        label=f"Download {field} Data ({year_from}–{year_to}) as CSV",
        data=df_live[["country_name", "count"]].to_csv(index=False).encode('utf-8'),
        file_name=f"{field.lower().replace(' ', '_')}_openalex_{year_from}_{year_to}.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.caption("Dashboard for thesis: Development of a dashboard for analyzing global scientific productivity (2010–2020)")
