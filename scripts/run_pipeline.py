#!/usr/bin/env python
"""
Chopard Pricing Analysis - Main Pipeline Runner

This script runs the complete ETL pipeline:
1. Extract: Load raw data from Excel or BigQuery
2. Transform: Clean and convert currencies
3. Load: Save to CSV and optionally BigQuery

Usage:
    python scripts/run_pipeline.py
    python scripts/run_pipeline.py --bigquery
"""

import os
import sys

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set Google Cloud credentials
if not os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'):
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'config/service_account.json'

from chopard.data_ingestion import load_local_data, fetch_bigquery_data
from chopard.processor import process_data, push_to_bigquery


def main(use_bigquery=False):
    """
    Main pipeline function.
    
    Args:
        use_bigquery: If True, fetch from BigQuery. If False, use local Excel file.
    """
    print("\n--- Starting Chopard Pricing Pipeline ---")
    print(f"Running in mode: {'BigQuery' if use_bigquery else 'Local File'}\n")
    
    # Step 1: Load raw data
    print("STEP 1/4: Loading raw data...")
    
    if use_bigquery:
        raw_df = fetch_bigquery_data()
    else:
        raw_df = load_local_data()
    
    print(f"  Loaded {len(raw_df)} raw records\n")
    
    # Step 2: Process data
    print("STEP 2/4: Processing data...")
    processed_df = process_data(raw_df)
    
    # Step 3: Save to CSV
    print("\nSTEP 3/4: Saving to CSV...")
    output_path = "data/final_processed_data.csv"
    processed_df.to_csv(output_path, index=False)
    print(f"  Saved to: {output_path}")
    
    # Step 4: Push to BigQuery (optional)
    if use_bigquery:
        print("\nSTEP 4/4: Uploading to BigQuery...")
        push_to_bigquery(processed_df, "chopard", "processed_chopard_data")
    else:
        print("\nSTEP 4/4: Skipping BigQuery upload (local mode)")
        print("  Run with --bigquery flag to upload")
    
    # Summary
    print("\n" + "="*60)
    print("PIPELINE COMPLETE")
    print("="*60)
    print(f"  Total watches: {len(processed_df)}")
    print(f"  Price range: {processed_df['price_eur'].min():,.0f} - {processed_df['price_eur'].max():,.0f} EUR")
    print(f"  Output file: {output_path}")
    
    # Collection breakdown
    print("\n  Collection breakdown:")
    collection_summary = processed_df.groupby('collection')['price_eur'].agg(['count', 'mean'])
    collection_summary.columns = ['Count', 'Avg Price']
    collection_summary = collection_summary.sort_values('Count', ascending=False).head(5)
    for col, row in collection_summary.iterrows():
        print(f"    - {col}: {int(row['Count'])} watches, avg {row['Avg Price']:,.0f} EUR")
    
    print("\nReady for analysis in Power BI!\n")
    
    return processed_df


if __name__ == "__main__":
    use_bq = '--bigquery' in sys.argv
    main(use_bigquery=use_bq)
