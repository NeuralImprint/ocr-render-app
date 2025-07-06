import pandas as pd

# Read the Excel file
df = pd.read_excel("Hand_table.xlsx")  # or pd.read_csv("ocr_table.csv")
from pymongo import MongoClient

# Local MongoDB
client = MongoClient("mongodb://localhost:27017/")

# Use or create a database
db = client["ocr_database"]

# Use or create a collection
collection = db["ocr_results"]
# Convert DataFrame rows to dictionary format
data_dict = df.to_dict(orient="records")

# Insert into MongoDB
collection.insert_many(data_dict)

print("Data inserted successfully!")
# View first few documents
for doc in collection.find().limit(5):
    print(doc)
def upload_to_mongo(file_path, db_name, collection_name):
    df = pd.read_excel(file_path)
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name]
    collection = db[collection_name]
    data_dict = df.to_dict(orient="records")
    collection.insert_many(data_dict)
    print("Upload complete!")

# Usage
upload_to_mongo("Hand_table.xlsx", "ocr_database", "ocr_results")

