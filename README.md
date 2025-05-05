# Background Remover Web Application

A web application that allows users to remove backgrounds from images with a simple drag-and-drop interface. The application uses the `rembg` library for automatic background removal and provides a modern, user-friendly interface.

## Features

- Drag and drop image upload
- Support for multiple image formats (PNG, JPG, JPEG, GIF, BMP, WEBP)
- Automatic background removal
- Real-time preview of original and processed images
- HD PNG output
- Modern, responsive UI

## Requirements

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository or download the source code.

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Drag and drop an image onto the upload area or click "Browse Files" to select an image

4. Wait for the processing to complete

5. The processed image will be displayed and automatically downloaded as a PNG file

## Notes

- Maximum file size: 16MB
- The application automatically detects the main subject in the image
- Output is always in PNG format with transparency
- Processing time may vary depending on the image size and complexity

## License

This project is open source and available under the MIT License. 