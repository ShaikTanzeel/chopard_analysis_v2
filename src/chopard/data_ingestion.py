# Data Ingestion: getting data from BQ or Excel


import pandas as pd
from io import StringIO
from google.cloud import bigquery
from chopard.config import PROJECT_ID, DATASET_ID


def fetch_bigquery_data(table_name="raw_pricing"):
    """
    Fetches raw data from BigQuery and parses the semicolon-delimited format.
    
    The data in BigQuery is stored as semicolon-separated values within a single column,
    so we need to parse it correctly before analysis.
    
    Returns:
        DataFrame with columns: brand, url, image_url, collection, reference_code, 
                               price, currency, country, life_span_date, category, scrapping_date
    """
    print(f"Connecting to BigQuery: {PROJECT_ID}.{DATASET_ID}.{table_name}...")
    
    # Connect to BigQuery
    client = bigquery.Client()
    
    # Query the raw table
    query = f"SELECT * FROM `{PROJECT_ID}.{DATASET_ID}.{table_name}`"
    raw_df = client.query(query).to_dataframe()
    
    print(f"  Found {len(raw_df)} raw rows")
    
    # The first column contains semicolon-delimited data
    first_col = raw_df.columns[0]
    raw_strings = raw_df[first_col].dropna().tolist()
    
    if raw_strings:
        # Combine rows into CSV format
        csv_content = "\n".join(raw_strings)
        
        # Parse with semicolon delimiter
        df = pd.read_csv(
            StringIO(csv_content), 
            sep=";",
            on_bad_lines='skip'
        )
        
        print(f"Parsed {len(df)} watch records")
        print(f"  Columns: {list(df.columns)}")
        return df
    else:
        raise ValueError("No data found in BigQuery table!")


def load_local_data(file_path="data/raw_chopard_data.csv.xlsx"):
    # Load from Excel but fix the weird spacing issues

    print(f"Loading local file: {file_path}...")
    
    # Read Excel file without header
    raw_df = pd.read_excel(file_path, header=None)
    print(f"  Raw Excel shape: {raw_df.shape}")
    
    # Merge all columns back together
    reconstructed_rows = []
    for idx, row in raw_df.iterrows():
        parts = [str(v) for v in row.values if pd.notna(v) and str(v) != 'nan']
        full_row = ','.join(parts)
        if full_row.strip():
            reconstructed_rows.append(full_row)
    
    print(f"  Reconstructed {len(reconstructed_rows)} rows")
    
    # Parse as semicolon-delimited CSV
    csv_content = "\n".join(reconstructed_rows)
    df = pd.read_csv(
        StringIO(csv_content), 
        sep=";",
        on_bad_lines='skip'
    )
    
    # Clean column names
    df.columns = [col.strip() for col in df.columns]
    
    print(f"Loaded {len(df)} records with columns: {list(df.columns)}")
    return df


if __name__ == "__main__":
    print("\n=== Testing Data Ingestion ===\n")
    
    df = load_local_data()
    print("\nSample data:")
    print(df.head())
    print(f"\nData types:\n{df.dtypes}")
