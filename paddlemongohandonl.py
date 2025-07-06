from paddleocr import PaddleOCR
import pandas as pd
from pymongo import MongoClient

# Step 1: Initialize PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang='en')
image_path = 'Excel.png'
result = ocr.ocr(image_path, cls=True)

# Step 2: Extract all text strings into a list
texts = [line[1][0] for line in result[0]]

# Step 3: Split into header and rows
num_cols = 4  # Adjust this if your table has a different number of columns
header = texts[:num_cols]
data_rows = [texts[i:i+num_cols] for i in range(num_cols, len(texts), num_cols)]

# Step 4: Create DataFrame
df = pd.DataFrame(data_rows, columns=header)
print(df)

# Step 5: Save as CSV (optional)
df.to_csv("structured_ocr_table.csv", index=False)

# Step 6: Push to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

# Convert to list of dictionaries and insert
records = df.to_dict(orient="records")
if records:
    collection.insert_many(records)
    print(f"✅ Inserted {len(records)} records into MongoDB.")
else:
    print("⚠️ No records to insert.")
