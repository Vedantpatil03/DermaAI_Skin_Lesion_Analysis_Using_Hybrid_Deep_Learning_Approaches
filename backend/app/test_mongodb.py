
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from the backend folder
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

MONGODB_URI = os.getenv("MONGODB_URI")

print("\n" + "=" * 40)
print("DERMAAI - MONGODB CONNECTION TEST")
print("=" * 40)

if not MONGODB_URI:
    print("ERROR: MONGODB_URI not found in .env")
    raise SystemExit(1)

client = None

try:
    client = MongoClient(
        MONGODB_URI,
        serverSelectionTimeoutMS=10000
    )

    # Test the connection
    client.admin.command("ping")

    # Select the DermaAI database
    db = client["dermaai"]

    print("SUCCESS: MongoDB connection established!")
    print(f"Database selected: {db.name}")
    print("Ready to build authentication and history.")

except Exception as error:
    print("ERROR: Could not connect to MongoDB.")
    print(f"Details: {error}")

finally:
    if client is not None:
        client.close()

print("=" * 40)
