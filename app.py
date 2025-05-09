from flask import Flask, request, send_file, jsonify, render_template
from rembg import remove
from PIL import Image
import io
import os

app = Flask(__name__)
app.debug = True  # Enable debug mode

@app.route('/')
def home():
    print("Home route accessed!")  # Debug print
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    try:
        # Process the image
        input_image = Image.open(file.stream).convert("RGBA")
        output_image = remove(input_image)
        
        # Save to bytes
        img_io = io.BytesIO()
        output_image.save(img_io, 'PNG')
        img_io.seek(0)
        
        return send_file(
            img_io,
            mimetype='image/png',
            as_attachment=True,
            download_name='removed_bg.png'
        )
    except Exception as e:
        print(f"Error processing image: {str(e)}")  # Debug print
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    import os
    from waitress import serve
    port = int(os.environ.get('PORT', 10000))
    print(f"Starting Waitress on port {port}...")
    serve(app, host='0.0.0.0', port=port) 