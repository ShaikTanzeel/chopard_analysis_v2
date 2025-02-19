from chopard.data_ingestion import fetch_bigquery_data
from chopard.data_processing import process_data
from chopard.exchange_rates.fetch_rates_new import get_exchange_rates
from chopard.exchange_rates.convert_new import convert_to_eur
from chopard.data_processing import push_to_bigquery

def main():
    print("\n🚀 Running Analysis Pipeline...\n")

    # Step 1: Fetch Data from BigQuery
    print("📥 Fetching Data from BigQuery...")
    bigquery_df = fetch_bigquery_data()
    print("✅ Data Ingested! Shape:", bigquery_df.shape)

    # Step 2: Process Data
    print("\n🔄 Processing Data...")
    processed_df = process_data(bigquery_df)  # Pass the dataframe
    print("✅ Data Processing Complete! Shape:", processed_df.shape)

    # Step 3: Fetch Exchange Rates
    print("\n💱 Fetching Exchange Rates...")
    rates_df = get_exchange_rates()
    print("✅ Exchange Rates Fetched! Shape:", rates_df.shape)

    # Step 4: Convert Prices to EUR
    print("\n💶 Converting Prices to EUR...")
    processed_df = convert_to_eur(processed_df, rates_df)
    print("✅ Currency Conversion Complete!")

    # Step 5: Save the final processed data
    processed_df.to_csv("data/final_processed_data.csv", index=False)
    print("✅ Final Data Saved to 'data/final_processed_data.csv'.")

    # Step 6: Push Processed Data to BigQuery
    print("\n🚀 Uploading Processed Data to BigQuery...")
    push_to_bigquery(processed_df, "luxurydata2502", "processed_chopard_data")
    print("✅ Data Successfully Pushed to BigQuery!")

if __name__ == "__main__":
    main()
