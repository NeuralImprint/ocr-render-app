import pandas as pd
from pymongo import MongoClient
import os

def upload_to_mongo(file_path, db_name, collection_name):
    # Detect file type
    ext = os.path.splitext(file_path)[1]
    
    if ext == ".csv":
        df = pd.read_csv(file_path)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(file_path, engine='openpyxl')
    else:
        raise ValueError("Unsupported file type.")

    records = df.to_dict(orient='records')

    # Connect to MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client[db_name]
    collection = db[collection_name]

    collection.insert_many(records)
    print(f"Uploaded {len(records)} records to {db_name}.{collection_name}")

# Example usage
upload_to_mongo("Hand_table.csv", "ocr_database", "ocr_results")
