import os
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
from rembg import remove
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import io
import cv2
import numpy as np

# Update for Vercel: set static and template folders
app = Flask(__name__, static_folder='../static', template_folder='../templates')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhance_image(image):
    # Convert PIL Image to OpenCV format
    img_array = np.array(image)
    img_cv = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
    
    # Convert to float32 for better precision
    img_float = img_cv.astype(np.float32) / 255.0
    
    # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
    lab = cv2.cvtColor(img_float, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l = clahe.apply((l * 255).astype(np.uint8))
    lab = cv2.merge([l, a, b])
    enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
    
    # Apply sharpening
    kernel = np.array([[-1,-1,-1], [-1,9,-1], [-1,-1,-1]])
    enhanced = cv2.filter2D(enhanced, -1, kernel)
    
    # Convert back to PIL Image
    enhanced = (enhanced * 255).astype(np.uint8)
    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB)
    enhanced_pil = Image.fromarray(enhanced)
    
    # Apply additional enhancements using PIL
    enhancer = ImageEnhance.Sharpness(enhanced_pil)
    enhanced_pil = enhancer.enhance(1.5)
    
    enhancer = ImageEnhance.Contrast(enhanced_pil)
    enhanced_pil = enhancer.enhance(1.2)
    
    enhancer = ImageEnhance.Brightness(enhanced_pil)
    enhanced_pil = enhancer.enhance(1.1)
    
    return enhanced_pil

def upscale_image(image, scale_factor=2):
    # Get original dimensions
    width, height = image.size
    
    # Calculate new dimensions
    new_width = int(width * scale_factor)
    new_height = int(height * scale_factor)
    
    # Upscale using Lanczos resampling
    upscaled = image.resize((new_width, new_height), Image.LANCZOS)
    
    # Apply sharpening to reduce blur
    enhancer = ImageEnhance.Sharpness(upscaled)
    upscaled = enhancer.enhance(1.5)
    
    return upscaled

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