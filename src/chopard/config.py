import os
from dotenv import load_dotenv

# Load the secrets from the .env file
load_dotenv()

# Define our settings
PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BIGQUERY_DATASET_ID")

# Check if they exist (Fail early if keys are missing)
if not PROJECT_ID:
    raise ValueError("GCP_PROJECT_ID is missing in .env file")
    
if not DATASET_ID:
    raise ValueError("BIGQUERY_DATASET_ID is missing in .env file")

print(f"Configuration Loaded: Project={PROJECT_ID}, Dataset={DATASET_ID}")
