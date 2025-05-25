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

### 2. Deep Learning Growth (2010–2020)

Script: `scripts/analyze_growth.py`

- Calculates percentage growth in publication counts from 2010 to 2020 for each country.
- Output: `data/raw/deep_learning_growth_2010_2020.csv`

### 3. Top 5 Growth Countries Chart

Script: `visualizations/top_growth_countries.py`

- Plots a bar chart for the top 5 countries with highest growth in Deep Learning research output.
- Output: `visualizations/outputs/top5_growth_dl.png`

---

## 🔄 AI Concept Analysis (`C154945302`)

### Scripts Added:

- `scripts/fetch_publication_counts_ai.py`: Fetches AI publication data (2010–2020) from OpenAlex.
- `scripts/analyze_growth_ai.py`: Computes growth rates for AI publications.
- `visualizations/ai_map_2020.py`: World map of AI publications in 2020.
- `visualizations/top_growth_countries_ai.py`: Bar chart of top 5 countries by AI growth.
- `visualizations/line_trend_countries.py`: Line chart for US, China, Germany research trends in AI and Deep Learning.
- `dashboard/app.py`: Streamlit-based dashboard to unify all components.

### 1. Fetch AI Publication Counts

Script: `scripts/fetch_publication_counts_ai.py`

- Fetches publication counts from OpenAlex API for concept: **Artificial Intelligence (C154945302)**
- Groups by country per year (2010–2020)
- Output CSV stored in: `data/raw/ai_publication_counts.csv`

### 2. AI Growth Analysis (2010–2020)

Script: `scripts/analyze_growth_ai.py`

- Calculates percentage growth in AI publication counts from 2010 to 2020.
- Output: `data/raw/ai_growth_2010_2020.csv`

### 3. AI World Map (2020)

Script: `visualizations/ai_map_2020.py`

- Generates a world map of AI research output by country for 2020.
- Output: `visualizations/outputs/ai_map_2020.html`

### 4. Top 5 AI Growth Countries (2010–2020)

Script: `visualizations/top_growth_countries_ai.py`

- Visualizes the top 5 countries by AI publication growth over the last decade.
- Output: `visualizations/outputs/top5_growth_ai.png`

### 5. Country Comparison: AI vs Deep Learning Trends

Script: `visualizations/line_trend_countries.py`

- Compares year-wise publication counts from 2010 to 2020 for US, China, and Germany.
- Covers both AI and Deep Learning fields.
- Output: `visualizations/outputs/line_trend_us_cn_de.png`
