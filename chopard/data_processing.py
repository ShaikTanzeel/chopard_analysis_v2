import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account
import os
from pandas_gbq import to_gbq


# Load environment variables
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
CREDENTIALS_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Authenticate with Google Cloud
credentials = service_account.Credentials.from_service_account_file(CREDENTIALS_PATH)
client = bigquery.Client(credentials=credentials, project=GCP_PROJECT_ID)

def process_data(df):
    """Process the fetched data by cleaning and filtering."""
    
    # Filter relevant columns
    df = df[['brand', 'collection', 'price', 'currency', 'country', 'life_span_date', 'price_before', 'price_difference', 'price_changed']]

    # Keep only selected currencies
    currencies_to_keep = ["USD", "EUR", "GBP", "HKD", "JPY", "CHF", "CNY", "TWD", "SGD", "KRW", "AED"]
    df = df[df['currency'].isin(currencies_to_keep)]

    # Map currency to country
    currency_to_country = {
        "USD": "US", "EUR": "EU", "GBP": "UK", "HKD": "HK",
        "JPY": "Japan", "CHF": "Switzerland", "CNY": "China",
        "TWD": "Taiwan", "SGD": "Singapore", "KRW": "South Korea", "AED": "UAE"
    }
    df['country'] = df['currency'].map(currency_to_country)

    # Remove null values in key columns
    df = df.dropna(subset=['price', 'price_before', 'collection'])

    # Save cleaned data
    df.to_csv("data/processed_data.csv", index=False)
    print("✅ Data processing complete. Saved as 'data/processed_data.csv'.")

    return df

def push_to_bigquery(df, dataset_id, table_id):
    """Uploads a Pandas DataFrame to Google BigQuery using pandas_gbq."""

    table_ref = f"{GCP_PROJECT_ID}.{dataset_id}.{table_id}"

    # Upload data
    to_gbq(df, destination_table=table_ref, project_id=GCP_PROJECT_ID, 
           credentials=credentials, if_exists="replace")  # ✅ Updated function
    
    print(f"✅ Data successfully pushed to BigQuery: {table_ref}")


if __name__ == "__main__":
    from chopard.data_ingestion import fetch_bigquery_data  # Import only when running directly
    df = fetch_bigquery_data()
    process_data(df)
