import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from nbconvert import HTMLExporter
from nbconvert.preprocessors import Preprocessor
from weasyprint import HTML
import io
import tempfile
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
ALLOWED_EXTENSIONS = {'ipynb'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
UPLOAD_FOLDER = tempfile.gettempdir()

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    """Check if the file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/', methods=['GET'])
def index():
    """Serve the main page."""
    return send_file('templates/index.html', mimetype='text/html')


@app.route('/image.png', methods=['GET'])
def serve_image():
    """Serve the profile image."""
    return send_file('image.png', mimetype='image/png')


@app.route('/robots.txt', methods=['GET'])
def serve_robots():
    """Serve the robots.txt file."""
    return send_file('robots.txt', mimetype='text/plain')


@app.route('/sitemap.xml', methods=['GET'])
def serve_sitemap():
    """Serve the sitemap.xml file."""
    return send_file('sitemap.xml', mimetype='application/xml')


@app.route('/api/convert', methods=['POST'])
def convert_ipynb_to_pdf():
    """Convert uploaded IPYNB file to PDF using HTML export and WeasyPrint for speed."""
    import json
    from jsonschema import validate, ValidationError
    # Minimal Jupyter notebook schema for validation
    notebook_schema = {
        "type": "object",
        "properties": {
            "cells": {"type": "array"},
            "metadata": {"type": "object"},
            "nbformat": {"type": "integer"},
            "nbformat_minor": {"type": "integer"}
        },
        "required": ["cells", "metadata", "nbformat", "nbformat_minor"]
    }
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .ipynb files are allowed'}), 400

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Validate notebook structure before conversion
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                notebook_json = json.load(f)
            validate(instance=notebook_json, schema=notebook_schema)
        except ValidationError as ve:
            os.remove(file_path)
            return jsonify({'error': f'Invalid notebook structure: {ve.message}'}), 400
        except Exception as ve:
            os.remove(file_path)
            return jsonify({'error': f'Invalid or corrupted notebook file: {str(ve)}'}), 400

        try:
            # Export notebook to HTML
            html_exporter = HTMLExporter()
            (body, resources) = html_exporter.from_filename(file_path)

            # Convert HTML to PDF using WeasyPrint
            pdf_io = io.BytesIO()
            HTML(string=body).write_pdf(pdf_io)
            pdf_io.seek(0)
            pdf_name = filename.rsplit('.', 1)[0] + '.pdf'

            # Clean up temp file
            os.remove(file_path)

            return send_file(
                pdf_io,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=pdf_name
            )
        except Exception as convert_error:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'Conversion failed: {str(convert_error)}. Please ensure your notebook is valid and try again.'}), 500
    except Exception as e:
        return jsonify({'error': f'Unexpected server error: {str(e)}'}), 500


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'}), 200


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File is too large. Maximum size is 50MB'}), 413


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
