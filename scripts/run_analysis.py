
import os
from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(".env")  # Ensure it's the correct path
load_dotenv(dotenv_path=dotenv_path)

print("🔍 GOOGLE_APPLICATION_CREDENTIALS:", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))
