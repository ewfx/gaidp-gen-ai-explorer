from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
from werkzeug.utils import secure_filename
import os
import threading


# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyC53wvzp-W7_IH_xrVjM0W8w6ywy8h8Op8"
genai.configure(api_key=GEMINI_API_KEY)

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend


UPLOAD_FOLDER = 'data'
ALLOWED_EXTENSIONS = {'csv', 'xlsx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Read Excel Data from 'data' folder
file_path = os.path.join(os.path.dirname(__file__), "data", "genAI_Data.xlsx")
EXCEL_DIR = os.path.join(os.path.dirname(__file__), "data")

# Check if file exists
def read_file(file_path):
    try:
        if file_path.endswith('.csv'):
            try:
                df = pd.read_csv(file_path, encoding='utf-8', engine='python')
            except UnicodeDecodeError:
                print("⚠ UnicodeDecodeError: Retrying with 'ISO-8859-1' encoding...")
                df = pd.read_csv(file_path, encoding='ISO-8859-1', engine='python')
        elif file_path.endswith(('.xls', '.xlsx','.csv')):
            try:
                df = pd.read_excel(file_path, engine='openpyxl')  # For XLSX files
            except ImportError:
                print("⚠ 'openpyxl' not found! Trying 'xlrd' for older Excel formats...")
                df = pd.read_excel(file_path, engine='xlrd')  # For older XLS files
        else:
            raise ValueError("❌ Unsupported file format. Please provide a CSV or Excel file.")
    except Exception as e:
        print(f"❌ Error reading file: {e}")
        return None

    return df


if not os.path.exists(file_path):
    print("File not found!")
else:
    df = read_file(file_path)
    #print("Data preview:\n", df.head())

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(directory, filename):
    """Check if file exists and generate a new unique name if needed."""
    base, ext = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    while os.path.exists(os.path.join(directory, new_filename)):
        new_filename = f"{base}_{counter}{ext}"
        counter += 1
    return new_filename


@app.route('/')
def home():
    return render_template("home.html")

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data_rules')
def data_rules():
    return render_template('data_rules.html')


@app.route('/upload_file')
def upload_file_page():
    return render_template('upload_file.html')


@app.route('/new_rule')
def new_rule():
    return render_template('new_rule.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        new_filename = get_unique_filename(app.config['UPLOAD_FOLDER'], filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], new_filename))
        return jsonify({"success": f"File uploaded successfully as {new_filename}"}), 200
    else:
        return jsonify({"error": "Invalid file type"}), 400

@app.route('/data')
def get_data():
    try:
        #df = pd.read_excel(file_path, dtype=str)  # Read as string to avoid NaN issues
        if not os.path.exists(file_path):
            print("File not found!")
        else:
            df = read_file(file_path)
            #print("Data preview:\n", df.head())

        if df.empty:
            return jsonify([])  # Return empty list if no data

        # Get column names dynamically
       # column_order = df.columns.tolist()  # Read column names in order

       # df = df[column_order]  # Preserve the order from Excel
        df = df.fillna("").astype(str).apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x)) # Replace NaN with empty string
        #print(df.head())
        #return jsonify(df.to_dict(orient='records'))  # Convert to JSON with correct order
        columns = df.columns.tolist()
        data = df.to_dict(orient='records')  # Convert data to JSON

        return jsonify({"columns": columns, "data": data})  # Send both columns and data
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/get-excel-templates', methods=['GET'])
def get_excel_templates():
    files = [
        {"name": f, "path": os.path.join(EXCEL_DIR, f)}
        for f in os.listdir(EXCEL_DIR) if f.endswith((".xlsx", ".xls",".csv"))
    ]
    return jsonify(files)

if __name__ == '__main__':
    app.run(port=5000,debug=True)
