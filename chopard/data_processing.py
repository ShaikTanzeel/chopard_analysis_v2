import pandas as pd
from chopard.data_ingestion import fetch_data_from_bigquery  # Import function

def process_data():
    """Process the fetched data by cleaning and filtering."""
    df = fetch_data_from_bigquery()

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
    df = df.dropna(subset=['price', 'price_before'])

    # Save cleaned data
    df.to_csv("data/processed_data.csv", index=False)
    print("✅ Data processing complete. Saved as 'data/processed_data.csv'.")

    return df

if __name__ == "__main__":
    process_data()
