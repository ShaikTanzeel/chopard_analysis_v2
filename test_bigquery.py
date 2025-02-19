import os
from dotenv import load_dotenv

from pathlib import Path
dotenv_path = Path(".env")  # Change path if needed
load_dotenv(dotenv_path=dotenv_path)


# Check if the variable is loaded
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not credentials_path:
    raise ValueError("❌ GOOGLE_APPLICATION_CREDENTIALS is not set or not found in .env file")

print(f"✅ Using credentials from: {credentials_path}")

# (Optional) Print all environment variables (for debugging)
# print(os.environ)



from google.cloud import bigquery

# Initialize BigQuery client
client = bigquery.Client()

# Define your query
query = """
    SELECT *  
    FROM `edhec-business-manageme.luxurydata2502.price-monitoring-2022`  
    LIMIT 10;
"""

# Execute query
query_job = client.query(query)  
results = query_job.result()  

# Convert results to DataFrame
df = results.to_dataframe()

# Print output
print(df)

