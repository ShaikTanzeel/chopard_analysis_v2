import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(".env")  # Ensure correct path
load_dotenv(dotenv_path=dotenv_path)

print("🔍 GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
print("🔍 GCP_PROJECT_ID:", os.getenv("GCP_PROJECT_ID"))

