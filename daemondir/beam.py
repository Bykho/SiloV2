import os
from pymongo import MongoClient
from datetime import datetime
from config import MONGODB_USERNAME, MONGODB_PASSWORD

# MongoDB Atlas connection string
MONGODB_CONNECTION_STRING = f"mongodb+srv://{MONGODB_USERNAME}:{MONGODB_PASSWORD}@<cluster-address>/<database>?retryWrites=true&w=majority"

# Connect to MongoDB Atlas
client = MongoClient(MONGODB_CONNECTION_STRING)
db = client.get_database("<database>")
collection = db.get_collection("<collection>")

def beam_to_cloud(folder_path):
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        # Extract metadata
        metadata = {
            "filename": filename,
            "path": file_path,
            "upload_date": datetime.utcnow(),
            # Add more metadata fields as needed
        }
        # Insert metadata into MongoDB
        collection.insert_one(metadata)
        print(f"Beamed {filename} to MongoDB Atlas.")

if __name__ == "__main__":
    # Path to the SH folder
    folder_path = os.path.expanduser("~/Desktop/SiloV2/SH")
    beam_to_cloud(folder_path)
