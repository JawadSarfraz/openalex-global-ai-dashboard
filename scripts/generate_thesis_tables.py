#!/usr/bin/env python3
"""
Generate LaTeX Tables for Thesis
This script creates comprehensive tables showing both publication counts and specialization ratios.
"""

import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.openalex_api import fetch_openalex_data, fetch_total_publications_by_country

def generate_latex_table(concept_id, concept_name, year_range=(2010, 2020), top_n=10):
    """
    Generate a LaTeX table with publication counts and specialization ratios.
    """
    print(f"Generating LaTeX table for {concept_name}...")
    
    # Fetch field-specific publications
    df_field = fetch_openalex_data(concept_id, year_range)
    
    # Fetch total publications for normalization
    df_total = fetch_total_publications_by_country(year_range)
    
    # Merge data
    df_merged = df_field.merge(df_total, on="country_code", how="left")
    
    # Calculate metrics
    total_field_pubs = df_merged["count"].sum()
    df_merged["share (%)"] = round((df_merged["count"] / total_field_pubs) * 100, 2)
    df_merged["specialization_ratio (%)"] = round((df_merged["count"] / df_merged["total_publications"]) * 100, 2)
    
    # Clean country codes
    df_merged["country_code"] = df_merged["country_code"].apply(lambda x: x.split("/")[-1] if isinstance(x, str) else x)
    
    # Get country names
    import pycountry
    def get_country_name(alpha2_code):
        try:
            return pycountry.countries.get(alpha_2=alpha2_code).name
        except:
            return alpha2_code
    
    df_merged["country_name"] = df_merged["country_code"].apply(get_country_name)
    
    # Sort by publication count for the main table
    df_merged = df_merged.sort_values("count", ascending=False)
    
    # Select top N countries
    df_top = df_merged.head(top_n).copy()
    
    # Format numbers for LaTeX
    df_top["count_formatted"] = df_top["count"].apply(lambda x: f"{x:,}")
    df_top["total_formatted"] = df_top["total_publications"].apply(lambda x: f"{x:,.0f}")
    df_top["share_formatted"] = df_top["share (%)"].apply(lambda x: f"{x:.2f}")
    df_top["specialization_formatted"] = df_top["specialization_ratio (%)"].apply(lambda x: f"{x:.2f}")
    
    return df_top

def create_latex_table(df, concept_name, year_range):
    """
    Create a LaTeX table string.
    """
    latex = f"""\\begin{{table}}[h]
\\centering
\\caption{{Top 10 Countries by {concept_name} Publications ({year_range[0]}--{year_range[1]}) with Specialization Analysis}}
\\label{{tab:{concept_name.lower().replace(' ', '_')}_specialization}}
\\begin{{tabular}}{{lrrrr}}
\\hline
\\textbf{{Country}} & \\textbf{{{concept_name} Publications}} & \\textbf{{Total Publications}} & \\textbf{{Share (\\%)}} & \\textbf{{Specialization (\\%)}} \\\\
\\hline
"""
    
    for _, row in df.iterrows():
        country = row["country_name"]
        count = row["count_formatted"]
        total = row["total_formatted"]
        share = row["share_formatted"]
        specialization = row["specialization_formatted"]
        
        latex += f"{country} & {count} & {total} & {share} & {specialization} \\\\\n"
    
    latex += """\\hline
\\end{tabular}
\\end{table}"""
    
    return latex

def main():
    """Generate LaTeX tables for both AI and Deep Learning."""
    
    # Define concepts
    concepts = {
        "C154945302": "Artificial Intelligence",
        "C108583219": "Deep Learning"
    }
    
    # Create output directory
    os.makedirs("thesis_tables", exist_ok=True)
    
    # Generate tables for each concept
    for concept_id, concept_name in concepts.items():
        print(f"\n{'='*60}")
        print(f"GENERATING LATEX TABLE: {concept_name}")
        print(f"{'='*60}")
        
        df_table = generate_latex_table(concept_id, concept_name)
        
        # Create LaTeX table
        latex_table = create_latex_table(df_table, concept_name, (2010, 2020))
        
        # Save to file
        output_file = f"thesis_tables/{concept_name.lower().replace(' ', '_')}_table.tex"
        with open(output_file, 'w') as f:
            f.write(latex_table)
        
        print(f"Saved LaTeX table to: {output_file}")
        
        # Display the table
        print(f"\nLaTeX Table for {concept_name}:")
        print(latex_table)
    
    # Create a combined analysis summary
    print(f"\n{'='*60}")
    print("COMBINED ANALYSIS SUMMARY")
    print(f"{'='*60}")
    
    # Generate both tables and compare
    ai_df = generate_latex_table("C154945302", "Artificial Intelligence")
    dl_df = generate_latex_table("C108583219", "Deep Learning")
    
    # Find countries that appear in both top 10 lists
    ai_countries = set(ai_df["country_name"])
    dl_countries = set(dl_df["country_name"])
    common_countries = ai_countries.intersection(dl_countries)
    
    print(f"Countries in both AI and Deep Learning top 10: {len(common_countries)}")
    for country in sorted(common_countries):
        ai_spec = ai_df[ai_df["country_name"] == country]["specialization_ratio (%)"].iloc[0]
        dl_spec = dl_df[dl_df["country_name"] == country]["specialization_ratio (%)"].iloc[0]
        print(f"  {country}: AI={ai_spec:.2f}%, DL={dl_spec:.2f}%")
    
    print(f"\n{'='*60}")
    print("LATEX TABLES GENERATION COMPLETE!")
    print(f"{'='*60}")
    print("Files saved in thesis_tables/")
    print("- artificial_intelligence_table.tex")
    print("- deep_learning_table.tex")

if __name__ == "__main__":
    main() 