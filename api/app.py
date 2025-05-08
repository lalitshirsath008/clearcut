import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import cv2
import numpy as np

# Set static and template folders for root-level folders
app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    if file and allowed_file(file.filename):
        # Read the image
        input_image = Image.open(file.stream)
        
        # Remove background only
        output_image = remove(input_image)
        
        # Save to bytes
        img_byte_arr = io.BytesIO()
        output_image.save(img_byte_arr, format='PNG')
        img_byte_arr.seek(0)
        
        return send_file(
            img_byte_arr,
            mimetype='image/png',
            as_attachment=True,
            download_name='removed_background.png'
        )
    
    return jsonify({'error': 'Invalid file type'}), 400

# No app.run() block here; Gunicorn will serve the app 