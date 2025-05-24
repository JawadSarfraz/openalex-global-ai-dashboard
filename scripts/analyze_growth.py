import pandas as pd
import os

INPUT_CSV = "data/raw/deep_learning_publication_counts.csv"
OUTPUT_CSV = "data/raw/deep_learning_growth_2010_2020.csv"

def compute_growth():
    df = pd.read_csv(INPUT_CSV)

    # Filter for years 2010 and 2020
    df_filtered = df[df["year"].isin([2010, 2020])].copy()

    # Extract short ISO country code
    df_filtered["country_short"] = df_filtered["country_code"].apply(lambda x: x.split("/")[-1])

    # Pivot by country code (short), columns = years
    df_pivot = df_filtered.pivot(index="country_short", columns="year", values="count").fillna(0)

    # Calculate growth percent
    df_pivot["growth_percent"] = ((df_pivot[2020] - df_pivot[2010]) / df_pivot[2010].replace(0, 1)) * 100
    df_pivot["growth_percent"] = df_pivot["growth_percent"].round(2)

    # Sort and save
    df_pivot = df_pivot.sort_values("growth_percent", ascending=False)
    df_pivot.to_csv(OUTPUT_CSV)
    print(f"Saved growth data to: {OUTPUT_CSV}")

if __name__ == "__main__":
    os.makedirs("data/raw", exist_ok=True)
    compute_growth()
