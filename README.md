# OpenAlex Global AI Dashboard

## Scripts

### 1. Fetch Deep Learning Publication Counts

Script: `scripts/fetch_publication_counts.py`

- Fetches publication counts from OpenAlex API for concept: **Deep Learning (C108583219)**
- Groups by country per year (2010–2020)
- Output CSV stored in: `data/raw/deep_learning_publication_counts.csv`

## Visualizations

### 1. Deep Learning World Map

Script: `visualizations/map_deep_learning_publications.py`

- Loads the publication count CSV
- Uses `folium` to generate a choropleth map of publication counts by country for the year 2020
- Output: `visualizations/outputs/deep_learning_map_2020.html`
