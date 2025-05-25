import pandas as pd
import matplotlib.pyplot as plt
import os

# Country ISO codes
COUNTRIES = ["US", "CN", "DE"]

# Paths
ai_path = "data/raw/ai_publication_counts.csv"
dl_path = "data/raw/deep_learning_publication_counts.csv"
output_path = "visualizations/outputs/line_trend_us_cn_de.png"

# Load & prepare data
def load_and_filter(path, label):
    df = pd.read_csv(path)
    df["country_short"] = df["country_code"].apply(lambda x: x.split("/")[-1])
    df_filtered = df[df["country_short"].isin(COUNTRIES)]
    df_filtered["field"] = label
    return df_filtered[["year", "country_short", "count", "field"]]

ai_df = load_and_filter(ai_path, "AI")
dl_df = load_and_filter(dl_path, "Deep Learning")

# Combine
df_all = pd.concat([ai_df, dl_df])

# Plot
plt.figure(figsize=(12, 6))
for country in COUNTRIES:
    for field in ["AI", "Deep Learning"]:
        subset = df_all[(df_all["country_short"] == country) & (df_all["field"] == field)]
        plt.plot(subset["year"], subset["count"], label=f"{country} - {field}")

plt.title("AI vs Deep Learning Research Trends (2010–2020)")
plt.xlabel("Year")
plt.ylabel("Publication Count")
plt.legend()
plt.grid(True)

# Save
os.makedirs("visualizations/outputs", exist_ok=True)
plt.savefig(output_path)
plt.close()
print(f"Saved line trend chart to {output_path}")
