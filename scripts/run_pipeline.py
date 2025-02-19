import pandas as pd
from chopard.data_ingestion import fetch_bigquery_data
from chopard.data_processing import process_data

def main():
    print("\n🚀 Running Analysis Pipeline...\n")

    # Step 1: Fetch Data
    print("📥 Fetching Data from BigQuery...")
    bigquery_df = fetch_bigquery_data()
    print("✅ Data Ingested! Shape:", bigquery_df.shape)

    # Step 2: Process Data
    print("\n🔄 Processing Data...")
    processed_df = process_data(bigquery_df)  # Pass the dataframe
    print("✅ Data Processing Complete! Shape:", processed_df.shape)

    # Step 3: Show Final Data
    print("\n✅ Final Processed DataFrame:")
    print(processed_df.head(10))

if __name__ == "__main__":
    main()
