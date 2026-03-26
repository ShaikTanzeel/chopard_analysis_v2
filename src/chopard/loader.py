import pandas as pd
from google.cloud import bigquery
from chopard.config import PROJECT_ID, DATASET_ID

def upload_raw_data_to_bigquery(csv_file_path, table_name):
    # Read Excel and dump it into BQ

    print(f"Reading data from {csv_file_path}...")
    df = pd.read_excel(csv_file_path)
    
    # Construct the full table ID: "project.dataset.table"
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"
    
    # Initialize the BigQuery Client
    client = bigquery.Client()
    
    # Define how we want to upload (Replace table if it exists)
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",  # Overwrite existing table
        source_format=bigquery.SourceFormat.CSV,
        autodetect=True,  # Let BigQuery guess if columns are numbers or text
    )

    print(f"Uploading to BigQuery table: {table_id}...")
    job = client.load_table_from_dataframe(df, table_id, job_config=job_config)
    
    # Wait for the job to finish
    job.result()
    
    print(f"Success! Loaded {job.output_rows} rows into {table_id}.")

if __name__ == "__main__":
    # This block allows us to run this script directly to test it
    upload_raw_data_to_bigquery("data/raw_chopard_data.csv.xlsx", "raw_pricing")