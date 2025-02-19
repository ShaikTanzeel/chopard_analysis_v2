import pandas as pd
from chopard.data_ingestion import fetch_data_from_bigquery
from chopard.data_processing import process_data

def main():
    print("\n🚀 Running Analysis Pipeline...\n")

    # Step 1: Fetch Data
    print("📥 Fetching Data from BigQuery...")
    bigquery_df = fetch_data_from_bigquery()
    print("✅ Data Ingested! Shape:", bigquery_df.shape)

    # Step 2: Process Data
    print("\n🔄 Processing Data...")
    processed_df, null_counts = process_data(bigquery_df)
    print("✅ Data Processing Complete! Shape:", processed_df.shape)

    # Step 3: Show Missing Values Check
    print("\n📊 Checking for missing values in critical columns:")
    print(null_counts)

    # Step 4: Show Final Data
    print("\n✅ Final Processed DataFrame:")
    print(processed_df.head(10))

if __name__ == "__main__":
    main()
