from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import google.generativeai as genai
import pandas as pd
from werkzeug.utils import secure_filename
import os
import threading
import logging

# Configure logging
logging.basicConfig(
    filename="flask_app.log",  # Log file name
    level=logging.INFO,  # Log level (DEBUG, INFO, WARNING, ERROR)
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyDGHu1_exPZmOuvqvnjZyjMa5ve9v8tSbQ"
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
        elif file_path.endswith(('.xls', '.xlsx')):
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

@app.route('/upload_file')
def upload_file_page():
    return render_template('upload_file.html')


@app.route('/new_rule')
def new_rule():
    return render_template('new_rule.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

@app.route('/datawithrules.html')
def data_with_rules():
    return render_template('datawithrules.html')

@app.route('/data_rules')
def data_rules():
    return render_template('data_rules.html')

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
        file_path = request.args.get("file")
        if not os.path.exists(file_path):
            print("File not found!")
        else:
            df = read_file(file_path)

        if df.empty:
            return jsonify([])

        df = df.fillna("").astype(str).apply(lambda col: col.map(lambda x: x.strip() if isinstance(x, str) else x)) # Replace NaN with empty string
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

@app.route("/get-rules")
def get_rules():
    """Fetch rules from the 'rules' sheet in the selected Excel file."""
    file_path = request.args.get("file")
    logging.info(f"file_path: {file_path}")

    if not file_path or not os.path.exists(file_path):
        return jsonify({"error": "File not found"}), 400

    try:
        # Read Excel file
        xls = pd.ExcelFile(file_path)

        # Check if "rules" sheet exists
        if "rules" not in xls.sheet_names:
            return jsonify({"error": "Rules are not generated, please generate first"}), 404

        df = pd.read_excel(xls, sheet_name="rules")

        if df.empty:
            return jsonify({"error": "Rules sheet is empty"}), 404

        return jsonify({
            "columns": df.columns.tolist(),
            "rows": df.values.tolist()
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5000,debug=True)
