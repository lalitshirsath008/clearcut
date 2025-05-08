# Background Remover

A beautiful web application that removes backgrounds from images using AI. Built with Flask and rembg.

## Features

- Drag and drop image upload
- Day/Night mode
- Mobile responsive design
- Real-time background removal
- Beautiful UI/UX

## Local Development

1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Run the application:
   ```bash
   python app.py
   ```
5. Open http://localhost:5000 in your browser

## Deployment on Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Use these settings:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn app:app`
   - **Python Version:** 3.9 or higher

## Production Deployment (Render/Waitress)

To deploy on Render using Waitress:

1. Make sure `waitress` is in your requirements.txt (already included).
2. Set the Render start command to:

```
waitress-serve --port=10000 app:app
```

This will serve your Flask app using Waitress on the port required by Render.

## Project Structure

```
.
├── app.py              # Main Flask application
├── requirements.txt    # Python dependencies
├── templates/         # HTML templates
│   └── index.html    # Main page template
└── README.md         # This file
```

## Technologies Used

- Flask - Web framework
- rembg - Background removal
- HTML/CSS/JavaScript - Frontend
- Gunicorn - Production server

## License

MIT License 