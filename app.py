from flask import Flask, request, render_template, session, redirect, url_for
import os
from werkzeug.utils import secure_filename
from paddleocr import PaddleOCR
import pandas as pd
from pymongo import MongoClient

app = Flask(__name__, static_url_path='/static', static_folder='static', template_folder='templates')
app.secret_key = 'ankit_secret'  # Needed for session handling

app.config['UPLOAD_FOLDER'] = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ocr = PaddleOCR(use_angle_cls=True, lang='en')

client = MongoClient("mongodb://localhost:27017/")
db = client["ocr_database"]
collection = db["ocr_results"]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def process_image_and_save_to_mongo(filepath):
    result = ocr.ocr(filepath, cls=True)
    texts = [line[1][0] for line in result[0]]
    num_cols = 4

    if len(texts) < num_cols:
        return None

    header = texts[:num_cols]
    data_rows = [texts[i:i + num_cols] for i in range(num_cols, len(texts), num_cols)]

    df = pd.DataFrame(data_rows, columns=header)
    records = df.to_dict(orient='records')
    collection.insert_many(records)
    return df

@app.route('/')
def index():
    # Show query result once, then clear it
    query_response = session.get('query_response', None)
    session['query_response'] = None  # Clear after displaying once
    return render_template('index.html', query_response=query_response)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return "No image uploaded", 400
    file = request.files['image']
    if file.filename == '':
        return "No selected file", 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        df = process_image_and_save_to_mongo(filepath)
        if df is not None:
            return df.to_html(classes='table', border=1)
        else:
            return "Failed to extract valid table from image."
    return "Invalid file format", 400

@app.route('/query', methods=['POST'])
def handle_query():
    user_input = request.form['user_query'].lower()

    name = None
    field = None
    possible_fields = ['name', 'age', 'marks', 'roll', 'roll_no']

    for word in user_input.split():
        if word.capitalize() in [doc.get("Name", "") for doc in collection.find()]:
            name = word.capitalize()
        for pf in possible_fields:
            if pf in word:
                field = pf

    if name and field:
        doc = collection.find_one({"Name": name})
        if doc:
            result = f"{field.capitalize()} of {name} is {doc.get(field.capitalize(), 'not found')}"
        else:
            result = f"No data found for {name}."
    else:
        result = "Couldn't interpret the query properly. Try 'marks of yash'."

    session['query_response'] = result
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

