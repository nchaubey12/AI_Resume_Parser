from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from resume_parser import parse_resume
from pdf_utils import extract_text_from_pdf
import os, json, uuid

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
DATA_FILE = "parsed_data.json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE) as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files.get("resume")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400

    filename = f"{uuid.uuid4()}_{file.filename}"
    path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(path)

    text = extract_text_from_pdf(path)
    parsed = parse_resume(text)
    parsed["resume_file"] = filename

    data = load_data()

    for d in data:
        if d.get("email") == parsed.get("email") and parsed.get("email"):
            return jsonify({"error": "Duplicate email"}), 400
        if d.get("phone") == parsed.get("phone") and parsed.get("phone"):
            return jsonify({"error": "Duplicate phone"}), 400

    data.append(parsed)
    save_data(data)

    return jsonify(parsed)

@app.route("/data")
def get_data():
    return jsonify(load_data())

@app.route("/resume/<filename>")
def get_resume(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route("/delete/<email>", methods=["DELETE"])
def delete_entry(email):
    data = [d for d in load_data() if d.get("email") != email]
    save_data(data)
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True)
