from paddleocr import PPStructure
from pymongo import MongoClient
import pandas as pd

# Step 1: Initialize OCR engine
ocr_engine = PPStructure(
    layout=True,
    show_log=True,
    table=True,
    ocr=True,
    lang='en',
    structure_version='PP-StructureV2'
)

# Step 2: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

# Step 3: Run OCR on the image
image_path = "Excel.png"
print(f"🔍 Processing: {image_path}")
result = ocr_engine(image_path)

# Step 4: Extract table and insert into MongoDB
for res in result:
    if 'res' in res and isinstance(res['res'], list):
        table_data = res['res']
        rows = []

        for row in table_data:
            if isinstance(row, list):
                cells = [cell['text'] for cell in row if isinstance(cell, dict) and 'text' in cell]
                if cells:
                    rows.append(cells)

        # If table has header and at least one row
        if len(rows) >= 2:
            df = pd.DataFrame(rows[1:], columns=rows[0])  # rows[0] is header
            df['source_image'] = image_path  # optional: track source

            records = df.to_dict(orient='records')
            if records:
                collection.insert_many(records)
                print(f"✅ Uploaded {len(records)} rows from {image_path} to MongoDB.")
            else:
                print(f"⚠️ No valid records extracted from {image_path}.")
        else:
            print(f"⚠️ Not enough table rows in {image_path} to build a DataFrame.")
