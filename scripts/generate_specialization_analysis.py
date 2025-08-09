#!/usr/bin/env python3
"""
Generate Specialization Analysis for AI and Deep Learning Research
This script creates comprehensive tables showing both publication counts and specialization ratios.
"""

import pandas as pd
import sys
import os

# Add parent directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.openalex_api import fetch_openalex_data, fetch_total_publications_by_country

def generate_specialization_table(concept_id, concept_name, year_range=(2010, 2020)):
    """
    Generate a comprehensive table with publication counts and specialization ratios.
    """
    print(f"Generating specialization analysis for {concept_name}...")
    
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
    
    # Sort by specialization ratio
    df_merged = df_merged.sort_values("specialization_ratio (%)", ascending=False)
    
    # Select and rename columns
    result_cols = [
        "country_name", 
        "count", 
        "total_publications", 
        "share (%)", 
        "specialization_ratio (%)"
    ]
    
    df_result = df_merged[result_cols].copy()
    df_result.columns = [
        "Country", 
        f"{concept_name} Publications", 
        "Total Publications", 
        f"{concept_name} Share (%)", 
        f"{concept_name} Specialization (%)"
    ]
    
    return df_result

def main():
    """Generate specialization analysis for both AI and Deep Learning."""
    
    # Define concepts
    concepts = {
        "C154945302": "Artificial Intelligence",
        "C108583219": "Deep Learning"
    }
    
    # Create output directory
    os.makedirs("data/analysis", exist_ok=True)
    
    # Generate analysis for each concept
    for concept_id, concept_name in concepts.items():
        print(f"\n{'='*60}")
        print(f"ANALYZING: {concept_name}")
        print(f"{'='*60}")
        
        df_analysis = generate_specialization_table(concept_id, concept_name)
        
        # Save to CSV
        output_file = f"data/analysis/{concept_name.lower().replace(' ', '_')}_specialization_analysis.csv"
        df_analysis.to_csv(output_file, index=False)
        print(f"Saved to: {output_file}")
        
        # Display top 10
        print(f"\nTop 10 Countries by {concept_name} Specialization:")
        print(df_analysis.head(10).to_string(index=False))
        
        # Display top 10 by publication count
        print(f"\nTop 10 Countries by {concept_name} Publication Count:")
        df_by_count = df_analysis.sort_values(f"{concept_name} Publications", ascending=False)
        print(df_by_count.head(10).to_string(index=False))
    
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE!")
    print(f"{'='*60}")
    print("Files saved in data/analysis/")
    print("- artificial_intelligence_specialization_analysis.csv")
    print("- deep_learning_specialization_analysis.csv")

if __name__ == "__main__":
    main() 