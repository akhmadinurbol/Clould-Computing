from flask import Flask, request, redirect, url_for, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1 MB limit
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def upload_form():
    return render_template_string('''
        <h2>File Sharing Application</h2>
        <form action="/upload" method="POST" enctype="multipart/form-data">
            <input type="file" name="file" required />
            <button type="submit">Upload File</button>
        </form>
    ''')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part', 400
    file = request.files['file']
    if file.filename == '' or not allowed_file(file.filename):
        return 'No selected file or file type not allowed', 400
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return f'File uploaded successfully: <a href="/uploads/{filename}">View File</a>'

if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create upload directory if it doesn't exist
    app.run(debug=True, port=5000)
