import sys
import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pycountry
import folium
import json
import streamlit.components.v1 as components
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.openalex_api import fetch_openalex_data, fetch_openalex_concepts, fetch_total_publications_by_country

st.set_page_config(layout="wide")
st.title("📊 Global Research Dashboard: AI & Deep Learning (2010–2020)")

# --- Simplified Field Selector ---
# Predefined concepts for AI and Deep Learning
PREDEFINED_CONCEPTS = {
    "Artificial Intelligence": "C154945302",
    "Deep Learning": "C108583219"
}

# Comment out the dynamic field selector 
# with st.spinner("Fetching available research fields from OpenAlex..."):
#     concepts = fetch_openalex_concepts(per_page=50, max_pages=5)
#     concept_options = {c["display_name"]: c["id"] for c in concepts}
# field_display = st.selectbox("Select Field of Research", list(concept_options.keys()))
# selected_concept_id = concept_options[field_display]

# New simplified field selector
field_display = st.selectbox("Select Field of Research", list(PREDEFINED_CONCEPTS.keys()))
selected_concept_id = PREDEFINED_CONCEPTS[field_display]

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

def get_country_name_from_short(short_code):
    """Convert short country codes to full country names"""
    try:
        return pycountry.countries.get(alpha_2=short_code).name
    except:
        return short_code

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

# Remove citation data fetching to simplify the dashboard

# --- Display Warning if Empty ---
if df_live.empty:
    st.warning("No data available for the selected year range.")
else:
    # --- Interactive Pie Chart ---
    st.subheader(f"Country Distribution - {field_display} Publications ({year_from}–{year_to})")
    
    # Prepare data for pie chart (top 10 countries + "Others")
    df_pie = df_live.sort_values(by="count", ascending=False).head(10).copy()
    others_count = df_live.sort_values(by="count", ascending=False).iloc[10:]["count"].sum()
    
    if others_count > 0:
        others_row = pd.DataFrame({
            "country_name": ["Others"],
            "count": [others_count],
            "share (%)": [round((others_count / total_count) * 100, 2)]
        })
        df_pie = pd.concat([df_pie, others_row], ignore_index=True)
    
    # Create interactive pie chart with Plotly
    fig_pie = px.pie(
        df_pie, 
        values="count", 
        names="country_name",
        title=f"Distribution of {field_display} Publications by Country ({year_from}–{year_to})",
        hover_data=["share (%)"],
        hole=0.3  # Create a donut chart
    )
    
    # Customize the pie chart
    fig_pie.update_traces(
        textposition='inside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                     "Publications: %{value}<br>" +
                     "Share: %{customdata[0]:.2f}%<br>" +
                     "<extra></extra>"
    )
    
    fig_pie.update_layout(
        height=500,
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # --- Interactive Bar Chart for Top Countries ---
    st.subheader(f"📊 Top Countries by Publication Count - {field_display}")
    
    # Prepare data for bar chart (top 10 countries)
    df_bar = df_live.sort_values(by="count", ascending=False).head(10)
    
    fig_bar = px.bar(
        df_bar,
        x="country_name",
        y="count",
        title=f"Top 10 Countries by {field_display} Publications ({year_from}–{year_to})",
        hover_data=["share (%)", "specialization_ratio"],
        color="count",
        color_continuous_scale="viridis"
    )
    
    fig_bar.update_traces(
        hovertemplate="<b>%{x}</b><br>" +
                     "Publications: %{y}<br>" +
                     "Share: %{customdata[0]:.2f}%<br>" +
                     "Specialization: %{customdata[1]:.2f}%<br>" +
                     "<extra></extra>",
        text=df_bar["count"].apply(lambda x: f"{x:,}"),
        textposition='auto'
    )
    
    fig_bar.update_layout(
        xaxis_title="Country",
        yaxis_title="Number of Publications",
        height=500,
        xaxis={'categoryorder':'total descending'}
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
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
        nan_fill_color="#ffffff",     # <<< No-data countries = WHITE
        nan_fill_opacity=1.0          
    ).add_to(m)

    folium.TileLayer(
        tiles="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
        attr="&copy; OpenStreetMap contributors &copy; CARTO",
        name="CartoDB Positron",
        control=False
    ).add_to(m)

    map_path = "visualizations/outputs/live_map.html"
    m.save(map_path)
    components.html(open(map_path, 'r', encoding='utf-8').read(), height=600, scrolling=True)

    # --- Table Display ---
    st.subheader(f"Publications by Country ({year_from}–{year_to}) - {field_display}")
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["Publication Counts", "Specialization Analysis"])
    
    with tab1:
        table_cols = ["country_name", "count", "share (%)"]
        st.dataframe(
            df_live[table_cols]
            .sort_values(by="count", ascending=False)
            .reset_index(drop=True)
        )
    
    with tab2:
        # Specialization analysis table
        specialization_cols = ["country_name", "count", "total_publications", "specialization_ratio"]
        df_specialization = df_live[specialization_cols].copy()
        df_specialization = df_specialization.sort_values(by="specialization_ratio", ascending=False).reset_index(drop=True)
        
        st.markdown("### Research Specialization Analysis")
        st.markdown("**Specialization Ratio** = (Field Publications / Total Publications) × 100")
        st.markdown("This shows which countries are truly specializing in this research field, regardless of their total research volume.")
        
        # Debug info
        st.write(f"Total countries in dataset: {len(df_specialization)}")
        st.write(f"Countries with count > 0: {len(df_specialization[df_specialization['count'] > 0])}")
        # st.write(f"Countries with specialization > 0: {len(df_specialization[df_specialization['specialization_ratio'] > 0])}")
        
        st.dataframe(df_specialization)
        
        # Show top 10 specialized countries
        st.markdown("### Top 10 Countries by Specialization")
        top_specialized = df_specialization.head(10)
        st.dataframe(top_specialized)
        
        # Create an interactive bar chart for top specialized countries
        fig_specialization = px.bar(
            top_specialized,
            x="specialization_ratio",
            y="country_name",
            orientation='h',
            title=f"Top 10 Countries by {field_display} Specialization ({year_from}–{year_to})",
            hover_data=["count", "total_publications"]
        )
        
        fig_specialization.update_traces(
            hovertemplate="<b>%{y}</b><br>" +
                         "Specialization: %{x:.2f}%<br>" +
                         "Field Publications: %{customdata[0]}<br>" +
                         "Total Publications: %{customdata[1]}<br>" +
                         "<extra></extra>",
            text=top_specialized["specialization_ratio"].apply(lambda x: f"{x:.2f}%"),
            textposition='auto'
        )
        
        fig_specialization.update_layout(
            xaxis_title="Specialization Ratio (%)",
            yaxis_title="Country",
            height=500
        )
        
        st.plotly_chart(fig_specialization, use_container_width=True)

    # --- Divider ---
    st.markdown("---")

    # --- Growth Chart ---
    st.subheader(f"📈 Top 5 Countries by Growth in {field_display} (2010–2020)")
    
    # Load growth data based on selected field
    if field_display == "Artificial Intelligence":
        growth_file = "data/raw/ai_growth_2010_2020.csv"
    else:  # Deep Learning
        growth_file = "data/raw/deep_learning_growth_2010_2020.csv"
    
    try:
        df_growth = pd.read_csv(growth_file)
        
        # Get top 5 countries by growth percentage
        top5_growth = df_growth.sort_values(by="growth_percent", ascending=False).head(5).copy()
        
        # Add full country names for better readability
        top5_growth["country_name"] = top5_growth["country_short"].apply(get_country_name_from_short)
        
        # Create interactive bar chart for growth
        fig_growth = px.bar(
            top5_growth,
            x="country_name",
            y="growth_percent",
            title=f"Top 5 Countries by Growth in {field_display} (2010–2020)",
            hover_data=["2010", "2020"],
            color="growth_percent",
            color_continuous_scale="viridis"
        )
        
        fig_growth.update_traces(
            hovertemplate="<b>%{x}</b><br>" +
                         "Growth: %{y:.0f}%<br>" +
                         "2010: %{customdata[0]} publications<br>" +
                         "2020: %{customdata[1]} publications<br>" +
                         "<extra></extra>",
            text=top5_growth["growth_percent"].apply(lambda x: f"{x:.0f}%"),
            textposition='auto'
        )
        
        fig_growth.update_layout(
            xaxis_title="Country",
            yaxis_title="Growth Percentage (%)",
            height=500
        )
        
        st.plotly_chart(fig_growth, use_container_width=True)
        
        # Display growth data table
        st.markdown("### 📊 Growth Data Table")
        growth_table_cols = ["country_name", "country_short", "2010", "2020", "growth_percent"]
        st.dataframe(
            top5_growth[growth_table_cols]
            .sort_values(by="growth_percent", ascending=False)
            .reset_index(drop=True)
        )
        
    except FileNotFoundError:
        st.warning(f"Growth data file not found: {growth_file}")
    except Exception as e:
        st.error(f"Error loading growth data: {str(e)}")

    # --- Divider ---
    st.markdown("---")

    # --- CSV Download ---
    st.subheader("Download Fetched Data (CSV)")
    
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
    st.caption("Dashboard for thesis: Development of dashboard for analyzing global scientific productivity (2010–2020)")
