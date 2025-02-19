import os
import pandas as pd
from google.cloud import bigquery
from dotenv import load_dotenv
import gdown
from pathlib import Path

dotenv_path = Path(".env")  # Change path if needed
load_dotenv(dotenv_path=dotenv_path)

# Authenticate Google Cloud credentials
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Initialize BigQuery client
client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))

def fetch_bigquery_data():
    """
    Fetches Chopard watch price data from Google BigQuery.
    """
    query = """
        SELECT * 
        FROM `edhec-business-manageme.luxurydata2502.price-monitoring-2022`
        WHERE brand = "Chopard"
    """
    query_job = client.query(query)
    df = query_job.to_dataframe()
    print("✅ BigQuery data successfully fetched!")
    return df

def download_google_drive_file():
    """
    Downloads the latest Chopard pricing data from Google Drive.
    """
    file_id = "1Hb3-HombnqBF5dS_govnrIo2InBOzKgR"
    output_file = "data/PM_EXTRACT_Chopard_Jan_2025.xlsx"

    # Ensure 'data' directory exists
    os.makedirs("data", exist_ok=True)

    # Download file
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

    # Load data
    xls = pd.ExcelFile(output_file)
    df_pm_extract = pd.read_excel(xls, sheet_name="Sheet1")
    print("✅ Google Drive file downloaded and loaded!")
    return df_pm_extract

def main():
    """
    Main function to execute data ingestion.
    """
    df_bigquery = fetch_bigquery_data()
    df_drive = download_google_drive_file()

    # Save fetched data (optional)
    df_bigquery.to_csv("data/bigquery_data.csv", index=False)
    df_drive.to_csv("data/drive_data.csv", index=False)
    print("✅ Data ingestion complete!")

if __name__ == "__main__":
    main()
