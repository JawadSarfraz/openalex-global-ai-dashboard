# OpenAlex Global AI Dashboard

## Overview

This project visualizes global research trends in **Artificial Intelligence** and **Deep Learning** using OpenAlex data. It supports both static snapshot analysis (CSV and HTML maps) and **live querying** from the OpenAlex API. The dashboard is implemented using **Streamlit**.

---

## Concepts Analyzed

- **Artificial Intelligence (C154945302)**
- **Deep Learning (C108583219)**

---

## Folder Structure

```
openalex-global-ai-dashboard/
├── dashboard/               # Streamlit app
│   └── app.py               # Main dashboard entry point
├── data/
│   └── raw/                 # Raw CSVs fetched from OpenAlex
├── scripts/                 # Data fetching and growth analysis scripts
├── services/                # Live API integration modules
│   └── openalex_api.py      # Query OpenAlex with filters
├── visualizations/          # Scripts to generate visualizations
    └── outputs/             # Charts and map HTMLs
```

---

## OpenAlex Live API Integration (NEW)

Script: `services/openalex_api.py`

- Dynamically fetches publication data from OpenAlex using `mailto`-compliant headers.

- Accepts:

  - Concept ID (AI or DL)
  - Year range (from slider input)

- Aggregates publication counts by country.

- Used by `dashboard/app.py` to show real-time data tables and CSV downloads.

---

## Data Fetching Scripts (Static CSV Mode)

### 1. Fetch Deep Learning Publication Counts

Script: `scripts/fetch_publication_counts.py`

- Concept: Deep Learning (C108583219)
- Groups by country per year (2010–2020)
- Output: `data/raw/deep_learning_publication_counts.csv`

### 2. Fetch AI Publication Counts

Script: `scripts/fetch_publication_counts_ai.py`

- Concept: AI (C154945302)
- Groups by country per year (2010–2020)
- Output: `data/raw/ai_publication_counts.csv`

---

## Growth Analysis Scripts

### 1. Deep Learning Growth (2010–2020)

Script: `scripts/analyze_growth.py`

- Calculates % growth in publication counts (2010–2020)
- Output: `data/raw/deep_learning_growth_2010_2020.csv`

### 2. AI Growth (2010–2020)

Script: `scripts/analyze_growth_ai.py`

- Output: `data/raw/ai_growth_2010_2020.csv`

---

## Visualization Scripts

### 1. Deep Learning World Map (2020)

Script: `visualizations/map_deep_learning_publications.py`

- Output: `visualizations/outputs/deep_learning_map_2020.html`

### 2. AI World Map (2020)

Script: `visualizations/ai_map_2020.py`

- Output: `visualizations/outputs/ai_map_2020.html`

### 3. Top 5 Growth Charts

- Deep Learning: `visualizations/top_growth_countries.py` ➞ `top5_growth_dl.png`
- AI: `visualizations/top_growth_countries_ai.py` ➞ `top5_growth_ai.png`

### 4. Trends in US, CN, DE

Script: `visualizations/line_trend_countries.py`

- Output: `visualizations/outputs/line_trend_us_cn_de.png`

---

## Streamlit Dashboard

Script: `dashboard/app.py`

Features:

- Dynamic year range selector (2010–2020)
- Realtime data fetch from OpenAlex
- Country code cleanup + name translation
- Sortable DataFrame view + CSV export
- Static map visualizations (2020)
- Growth charts and trendlines

### Run the Dashboard

```bash
streamlit run dashboard/app.py
```

---

## Next Steps (Planned)

- Choropleth map for live data
- Add full country names (✅ Done)
- Sortable publication table with % shares
- Year-over-year growth animation (optional)
- Concept ID search input
- Deployment on cloud (with HTTPS)

---

## Maintainer

Jawwad Sarfraz
MSc Thesis, Kiel University
Topic: "Dashboard for analyzing global scientific productivity using OpenAlex"
