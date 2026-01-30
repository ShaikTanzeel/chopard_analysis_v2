"""
Data Processing Module
Handles cleaning, transforming, and currency conversion of watch data.
"""

import pandas as pd
from google.cloud import bigquery
from chopard.config import PROJECT_ID, DATASET_ID
from chopard.exchange import get_exchange_rates


def clean_data(df):
    """
    Cleans the raw watch data by handling missing values and fixing data types.
    
    Steps:
    1. Remove rows with NULL prices
    2. Remove rows without currency
    3. Convert price strings to numbers
    4. Remove duplicate entries
    """
    print("Cleaning data...")
    initial_count = len(df)
    
    df = df.copy()
    
    # Remove NULL prices
    df = df[df['price'].notna()]
    df = df[df['price'] != 'NULL']
    df = df[df['price'] != 'null']
    print(f"  After removing NULL prices: {len(df)} rows")
    
    # Remove rows without currency
    df = df[df['currency'].notna()]
    print(f"  After removing missing currencies: {len(df)} rows")
    
    # Convert price to numeric (remove commas and spaces)
    df['price'] = df['price'].astype(str).str.replace(',', '').str.replace(' ', '')
    df['price'] = pd.to_numeric(df['price'], errors='coerce')
    df = df[df['price'].notna()]
    print(f"  After converting price to numeric: {len(df)} rows")
    
    # Remove duplicates
    df = df.drop_duplicates(subset=['reference_code', 'country'], keep='first')
    print(f"  After removing duplicates: {len(df)} rows")
    
    # Clean collection names
    if 'collection' in df.columns:
        df['collection'] = df['collection'].str.replace('"', '').str.strip()
    
    print(f"Cleaning complete! Kept {len(df)}/{initial_count} rows ({len(df)/initial_count*100:.1f}%)")
    
    return df


def convert_prices_to_eur(df, rates_dict):
    """
    Converts all prices to EUR using exchange rates.
    
    Why EUR? It's a stable currency and Chopard is a European brand,
    so it makes sense to compare all prices in EUR.
    """
    print("Converting prices to EUR...")
    
    df = df.copy()
    
    # Apply conversion to each row
    df['price_eur'] = df.apply(
        lambda row: convert_single_price(row['price'], row['currency'], rates_dict),
        axis=1
    )
    
    success_count = df['price_eur'].notna().sum()
    print(f"Converted {success_count}/{len(df)} prices to EUR")
    
    print("\n  Currency distribution:")
    print(df['currency'].value_counts().head(10).to_string())
    
    return df


def convert_single_price(price, currency, rates_dict):
    """
    Converts a single price to EUR.
    
    The exchange rate tells us: 1 EUR = X currency
    So to convert: price_eur = price / rate
    """
    if pd.isna(price) or pd.isna(currency):
        return None
    
    currency = currency.upper().strip()
    
    # Already EUR, no conversion needed
    if currency == 'EUR':
        return price
    
    rate = rates_dict.get(currency)
    if rate is None:
        return None
    
    return round(price / rate, 2)


def process_data(df):
    """
    Main processing pipeline: Clean -> Get Rates -> Convert Currency
    """
    print("\n" + "="*50)
    print("STARTING DATA PROCESSING")
    print("="*50 + "\n")
    
    # Step 1: Clean the data
    df = clean_data(df)
    
    # Step 2: Get exchange rates
    print("\nFetching exchange rates...")
    rates = get_exchange_rates()
    
    # Step 3: Convert prices to EUR
    df = convert_prices_to_eur(df, rates)
    
    # Step 4: Remove rows that couldn't be converted
    df = df[df['price_eur'].notna()]
    
    print(f"\nProcessing complete!")
    print(f"  Final dataset: {len(df)} watches")
    print(f"  Price range: {df['price_eur'].min():,.0f} - {df['price_eur'].max():,.0f} EUR")
    print(f"  Average price: {df['price_eur'].mean():,.0f} EUR")
    
    return df


def push_to_bigquery(df, dataset_id, table_name):
    """
    Uploads processed data back to BigQuery.
    This allows Power BI to connect directly to the cleaned data.
    """
    print(f"\nPushing to BigQuery: {PROJECT_ID}.{dataset_id}.{table_name}...")
    
    client = bigquery.Client()
    table_id = f"{PROJECT_ID}.{dataset_id}.{table_name}"
    
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )
    
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    job.result()
    
    print(f"Successfully pushed {len(df)} rows to {table_id}")


if __name__ == "__main__":
    from chopard.data_ingestion import load_local_data
    
    print("\n=== Testing Data Processing ===\n")
    
    # Load raw data
    raw_df = load_local_data()
    
    # Process it
    processed_df = process_data(raw_df)
    
    # Show sample
    print("\nSample of processed data:")
    print(processed_df[['collection', 'reference_code', 'price', 'currency', 'country', 'price_eur']].head(10))