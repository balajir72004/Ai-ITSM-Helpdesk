import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Load .env from the project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_DATABASE = os.getenv(
    "MONGODB_DATABASE",
    "itsm_helpdesk",
)

if not MONGODB_URI:
    raise RuntimeError(
        "MONGODB_URI is missing. Check the .env file."
    )

# Create MongoDB client with TLS certificate verification
client = MongoClient(
    MONGODB_URI,
    tls=True,
    serverSelectionTimeoutMS=15000,
    connectTimeoutMS=15000,
)

# Select database
db = client[MONGODB_DATABASE]

# Application collections
tickets_collection = db["tickets"]
software_requests_collection = db["software_requests"]
audit_logs_collection = db["audit_logs"]


def test_connection():
    """Check whether MongoDB Atlas is reachable."""
    try:
        client.admin.command("ping")

        print("MongoDB Atlas connection successful!")
        print(f"Database: {MONGODB_DATABASE}")

        return True

    except PyMongoError as error:
        print("MongoDB Atlas connection failed.")
        print(f"Error: {error}")

        return False


if __name__ == "__main__":
    test_connection()
    client.close()