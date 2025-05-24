import pandas as pd
import matplotlib.pyplot as plt
import os

INPUT_CSV = "data/raw/deep_learning_growth_2010_2020.csv"
OUTPUT_IMG = "visualizations/outputs/top5_growth_dl.png"

def plot_top_5_growth():
    df = pd.read_csv(INPUT_CSV, index_col=0)

    # Pick top 5
    top5 = df.head(5)

    # Plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(top5.index, top5["growth_percent"])
    plt.title("Top 5 Countries by Deep Learning Publication Growth (2010–2020)")
    plt.xlabel("Country Code")
    plt.ylabel("Growth (%)")
    plt.grid(True)

    os.makedirs("visualizations/outputs", exist_ok=True)
    plt.savefig(OUTPUT_IMG)
    plt.close()
    print(f"Saved plot to {OUTPUT_IMG}")

if __name__ == "__main__":
    plot_top_5_growth()
