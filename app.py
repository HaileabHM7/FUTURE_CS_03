import os
from flask import Flask, request, render_template, send_file
from crypto_utils import encrypt_file, decrypt_file
from dotenv import load_dotenv
from io import BytesIO

load_dotenv()

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    encrypted_data = encrypt_file(file.read())

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(encrypted_data)

    return "File uploaded and encrypted successfully"

@app.route("/download/<filename>")
def download(filename):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, "rb") as f:
        decrypted_data = decrypt_file(f.read())

    return send_file(
        BytesIO(decrypted_data),
        download_name=filename,
        as_attachment=True
    )

if __name__ == "__main__":
    app.run(debug=True)
