import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Check if the variable is loaded
credentials_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

if not credentials_path:
    raise ValueError("❌ GOOGLE_APPLICATION_CREDENTIALS is not set or not found in .env file")

print(f"✅ Using credentials from: {credentials_path}")

# (Optional) Print all environment variables (for debugging)
# print(os.environ)
