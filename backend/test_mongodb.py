
import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv(Path(__file__).resolve().parent / ".env")

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

    client.admin.command("ping")
    db = client["dermaai"]

    print("SUCCESS: MongoDB connection established!")
    print(f"Database selected: {db.name}")

except Exception as error:
    print("ERROR: Could not connect to MongoDB.")
    print(f"Details: {error}")

finally:
    if client is not None:
        client.close()

print("=" * 40)
