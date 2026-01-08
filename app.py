import os
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from nbconvert import PDFExporter
from nbconvert.preprocessors import Preprocessor
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


@app.route('/api/convert', methods=['POST'])
def convert_ipynb_to_pdf():
    """Convert uploaded IPYNB file to PDF."""
    try:
        # Check if file is in request
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']

        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # Check file extension
        if not allowed_file(file.filename):
            return jsonify({'error': 'Only .ipynb files are allowed'}), 400

        # Read file content
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Convert to PDF
        try:
            pdf_exporter = PDFExporter()
            (pdf_output, _) = pdf_exporter.from_filename(file_path)

            # Clean up temp file
            os.remove(file_path)

            # Create response with PDF
            pdf_io = io.BytesIO(pdf_output)
            pdf_name = filename.rsplit('.', 1)[0] + '.pdf'

            return send_file(
                pdf_io,
                mimetype='application/pdf',
                as_attachment=True,
                download_name=pdf_name
            )

        except Exception as convert_error:
            # Clean up temp file
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': f'Conversion failed: {str(convert_error)}'}), 500

    except Exception as e:
        return jsonify({'error': str(e)}), 500


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
