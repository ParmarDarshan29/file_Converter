
import os
import io
import shutil
import zipfile
import subprocess
import tempfile
import sqlite3
import json
import csv
from datetime import datetime, timedelta
from functools import wraps
from flask import Flask, request, send_file, jsonify, session, render_template_string
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
from nbconvert import HTMLExporter
from weasyprint import HTML
from docx import Document
from openpyxl import load_workbook
from pptx import Presentation
from PIL import Image
import img2pdf
from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import pypandoc
import markdown2
import pdfkit
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from bs4 import BeautifulSoup
import yaml

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
CORS(app)
bcrypt = Bcrypt(app)

# Flask-Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Rate limiting
limiter = Limiter(
	app=app,
	key_func=get_remote_address,
	default_limits=["200 per day", "50 per hour"],
	storage_uri="memory://"
)

# Configuration
ALLOWED_EXTENSIONS = {
	# Documents
	'txt', 'rtf', 'odt', 'docx', 'doc', 'pdf',
	# Spreadsheets
	'xlsx', 'xls', 'csv', 'ods',
	# Presentations
	'pptx', 'ppt', 'odp',
	# Images
	'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'svg', 'ico', 'heic',
	# Web
	'html', 'htm', 'mhtml',
	# Notebooks
	'ipynb',
	# Code
	'py', 'js', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'json', 'xml', 'yaml', 'yml',
	# LaTeX
	'tex', 'latex',
	# Markup
	'md', 'markdown', 'rst'
}

MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB
UPLOAD_FOLDER = tempfile.gettempdir()
DATABASE = 'users.db'

app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Database setup
def init_db():
	"""Initialize the SQLite database."""
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('''
		CREATE TABLE IF NOT EXISTS users (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			username TEXT UNIQUE NOT NULL,
			email TEXT UNIQUE NOT NULL,
			password TEXT NOT NULL,
			created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
		)
	''')
	c.execute('''
		CREATE TABLE IF NOT EXISTS conversion_history (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			user_id INTEGER,
			filename TEXT,
			file_type TEXT,
			converted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
			FOREIGN KEY (user_id) REFERENCES users (id)
		)
	''')
	conn.commit()
	conn.close()

# User class for Flask-Login
class User(UserMixin):
	def __init__(self, id, username, email):
		self.id = id
		self.username = username
		self.email = email

@login_manager.user_loader
def load_user(user_id):
	"""Load user from database."""
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
	user = c.fetchone()
	conn.close()
	if user:
		return User(user[0], user[1], user[2])
	return None

def allowed_file(filename):
	"""Check if the file extension is allowed."""
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename):
	"""Get file extension in lowercase."""
	return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

# Conversion functions
def convert_image_to_pdf(file_path):
	"""Convert image to PDF using img2pdf."""
	with open(file_path, 'rb') as f:
		pdf_bytes = img2pdf.convert(f.read())
	return io.BytesIO(pdf_bytes)

def convert_text_to_pdf(file_path):
	"""Convert plain text file to PDF."""
	pdf_io = io.BytesIO()
	doc = SimpleDocTemplate(pdf_io, pagesize=letter)
	styles = getSampleStyleSheet()
	story = []
    
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
		text = f.read()
		# Use Preformatted to preserve formatting
		pre_style = ParagraphStyle(
			'CustomCode',
			parent=styles['Code'],
			fontSize=9,
			leading=11,
			fontName='Courier'
		)
		lines = text.split('\n')
		for line in lines[:1000]:  # Limit to first 1000 lines for performance
			p = Preformatted(line, pre_style)
			story.append(p)
    
	doc.build(story)
	pdf_io.seek(0)
	return pdf_io

def convert_docx_to_pdf(file_path):
	"""Convert DOCX to PDF using LibreOffice."""
	output_dir = os.path.dirname(file_path)
	try:
		subprocess.run(
			['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', output_dir, file_path],
			check=True,
			capture_output=True,
			timeout=60
		)
		pdf_path = file_path.rsplit('.', 1)[0] + '.pdf'
		with open(pdf_path, 'rb') as f:
			pdf_io = io.BytesIO(f.read())
		os.remove(pdf_path)
		return pdf_io
	except Exception as e:
		raise Exception(f"LibreOffice conversion failed: {str(e)}")

def convert_xlsx_to_pdf(file_path):
	"""Convert Excel to PDF using LibreOffice."""
	return convert_docx_to_pdf(file_path)

def convert_pptx_to_pdf(file_path):
	"""Convert PowerPoint to PDF using LibreOffice."""
	return convert_docx_to_pdf(file_path)

def convert_csv_to_pdf(file_path):
	"""Convert CSV to PDF."""
	pdf_io = io.BytesIO()
	doc = SimpleDocTemplate(pdf_io, pagesize=A4)
	styles = getSampleStyleSheet()
	story = []
    
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
		reader = csv.reader(f)
		for row in reader:
			text = ', '.join(row)
			p = Paragraph(text, styles['Normal'])
			story.append(p)
			story.append(Spacer(1, 0.1*inch))
    
	doc.build(story)
	pdf_io.seek(0)
	return pdf_io

def convert_html_to_pdf(file_path):
	"""Convert HTML to PDF using weasyprint."""
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
		html_content = f.read()
	pdf_io = io.BytesIO()
	HTML(string=html_content).write_pdf(pdf_io)
	pdf_io.seek(0)
	return pdf_io

def convert_markdown_to_pdf(file_path):
	"""Convert Markdown to PDF."""
	with open(file_path, 'r', encoding='utf-8') as f:
		md_content = f.read()
	html_content = markdown2.markdown(md_content)
	html_full = f"<html><body>{html_content}</body></html>"
	pdf_io = io.BytesIO()
	HTML(string=html_full).write_pdf(pdf_io)
	pdf_io.seek(0)
	return pdf_io

def convert_ipynb_to_pdf(file_path):
	"""Convert Jupyter Notebook to PDF."""
	html_exporter = HTMLExporter()
	(body, resources) = html_exporter.from_filename(file_path)
	pdf_io = io.BytesIO()
	HTML(string=body).write_pdf(pdf_io)
	pdf_io.seek(0)
	return pdf_io

def convert_latex_to_pdf(file_path):
	"""Convert LaTeX to PDF using pdflatex."""
	output_dir = os.path.dirname(file_path)
	try:
		# Run pdflatex
		result = subprocess.run(
			['pdflatex', '-output-directory', output_dir, '-interaction=nonstopmode', file_path],
			capture_output=True,
			timeout=60,
			cwd=output_dir
		)
		pdf_path = file_path.rsplit('.', 1)[0] + '.pdf'
		if os.path.exists(pdf_path):
			with open(pdf_path, 'rb') as f:
				pdf_io = io.BytesIO(f.read())
			# Cleanup auxiliary files
			base_name = os.path.splitext(file_path)[0]
			for ext in ['.aux', '.log', '.out', '.pdf']:
				aux_file = base_name + ext
				if os.path.exists(aux_file):
					os.remove(aux_file)
			return pdf_io
		else:
			raise Exception("PDF not generated")
	except Exception as e:
		raise Exception(f"LaTeX conversion failed: {str(e)}")

def convert_code_to_pdf(file_path, extension):
	"""Convert code files to PDF with syntax highlighting."""
	pdf_io = io.BytesIO()
	doc = SimpleDocTemplate(pdf_io, pagesize=letter)
	styles = getSampleStyleSheet()
	story = []
    
	code_style = ParagraphStyle(
		'Code',
		parent=styles['Code'],
		fontSize=8,
		leading=10,
		fontName='Courier',
		leftIndent=10
	)
    
	# Add title
	title = Paragraph(f"Code File: {os.path.basename(file_path)}", styles['Title'])
	story.append(title)
	story.append(Spacer(1, 0.3*inch))
    
	with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
		lines = f.readlines()
		for i, line in enumerate(lines[:1000], 1):  # Limit to 1000 lines
			line_with_number = f"{i:4d} | {line.rstrip()}"
			p = Preformatted(line_with_number, code_style)
			story.append(p)
    
	doc.build(story)
	pdf_io.seek(0)
	return pdf_io

def convert_json_to_pdf(file_path):
	"""Convert JSON to PDF."""
	with open(file_path, 'r', encoding='utf-8') as f:
		data = json.load(f)
	formatted_json = json.dumps(data, indent=2)
    
	# Create temp text file
	temp_txt = file_path + '.txt'
	with open(temp_txt, 'w') as f:
		f.write(formatted_json)
    
	pdf_io = convert_text_to_pdf(temp_txt)
	os.remove(temp_txt)
	return pdf_io

def convert_yaml_to_pdf(file_path):
	"""Convert YAML to PDF."""
	with open(file_path, 'r', encoding='utf-8') as f:
		data = yaml.safe_load(f)
	formatted_yaml = yaml.dump(data, default_flow_style=False)
    
	temp_txt = file_path + '.txt'
	with open(temp_txt, 'w') as f:
		f.write(formatted_yaml)
    
	pdf_io = convert_text_to_pdf(temp_txt)
	os.remove(temp_txt)
	return pdf_io

def convert_file_to_pdf(file_path, extension):
	"""Main conversion router."""
	# Image formats
	if extension in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'tif', 'webp', 'ico', 'heic']:
		return convert_image_to_pdf(file_path)
    
	# Microsoft Office formats
	elif extension in ['docx', 'doc', 'odt', 'rtf']:
		return convert_docx_to_pdf(file_path)
    
	elif extension in ['xlsx', 'xls', 'ods']:
		return convert_xlsx_to_pdf(file_path)
    
	elif extension in ['pptx', 'ppt', 'odp']:
		return convert_pptx_to_pdf(file_path)
    
	# Text and markup
	elif extension == 'csv':
		return convert_csv_to_pdf(file_path)
    
	elif extension == 'txt':
		return convert_text_to_pdf(file_path)
    
	elif extension in ['html', 'htm', 'mhtml']:
		return convert_html_to_pdf(file_path)
    
	elif extension in ['md', 'markdown']:
		return convert_markdown_to_pdf(file_path)
    
	elif extension == 'ipynb':
		return convert_ipynb_to_pdf(file_path)
    
	elif extension in ['tex', 'latex']:
		return convert_latex_to_pdf(file_path)
    
	elif extension == 'json':
		return convert_json_to_pdf(file_path)
    
	elif extension in ['yaml', 'yml']:
		return convert_yaml_to_pdf(file_path)
    
	# Code files
	elif extension in ['py', 'js', 'java', 'cpp', 'c', 'cs', 'php', 'rb', 'go', 'rs', 'swift', 'kt', 'xml', 'rst']:
		return convert_code_to_pdf(file_path, extension)
    
	# PDF (return as-is or optimize)
	elif extension == 'pdf':
		with open(file_path, 'rb') as f:
			return io.BytesIO(f.read())
    
	else:
		raise Exception(f"Unsupported file format: {extension}")

# Routes
@app.route('/', methods=['GET'])
def index():
	"""Serve the main page."""
	return send_file('templates/index.html', mimetype='text/html')

@app.route('/image.png', methods=['GET'])
def serve_image():
	"""Serve the profile image."""
	if os.path.exists('image.png'):
		return send_file('image.png', mimetype='image/png')
	return '', 404

@app.route('/robots.txt', methods=['GET'])
def serve_robots():
	"""Serve the robots.txt file."""
	if os.path.exists('robots.txt'):
		return send_file('robots.txt', mimetype='text/plain')
	return '', 404

@app.route('/sitemap.xml', methods=['GET'])
def serve_sitemap():
	"""Serve the sitemap.xml file."""
	if os.path.exists('sitemap.xml'):
		return send_file('sitemap.xml', mimetype='application/xml')
	return '', 404

@app.route('/api/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
	"""Register a new user."""
	data = request.get_json()
	username = data.get('username', '').strip()
	email = data.get('email', '').strip()
	password = data.get('password', '')
    
	if not username or not email or not password:
		return jsonify({'error': 'All fields are required'}), 400
    
	if len(password) < 6:
		return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
	hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
	try:
		conn = sqlite3.connect(DATABASE)
		c = conn.cursor()
		c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
				  (username, email, hashed_password))
		conn.commit()
		user_id = c.lastrowid
		conn.close()
        
		user = User(user_id, username, email)
		login_user(user)
        
		return jsonify({
			'message': 'Registration successful',
			'user': {'id': user_id, 'username': username, 'email': email}
		}), 201
	except sqlite3.IntegrityError:
		return jsonify({'error': 'Username or email already exists'}), 400

@app.route('/api/login', methods=['POST'])
@limiter.limit("10 per hour")
def login():
	"""Login user."""
	data = request.get_json()
	username = data.get('username', '').strip()
	password = data.get('password', '')
    
	if not username or not password:
		return jsonify({'error': 'Username and password are required'}), 400
    
	conn = sqlite3.connect(DATABASE)
	c = conn.cursor()
	c.execute('SELECT id, username, email, password FROM users WHERE username = ?', (username,))
	user_data = c.fetchone()
	conn.close()
    
	if user_data and bcrypt.check_password_hash(user_data[3], password):
		user = User(user_data[0], user_data[1], user_data[2])
		login_user(user)
		return jsonify({
			'message': 'Login successful',
			'user': {'id': user_data[0], 'username': user_data[1], 'email': user_data[2]}
		}), 200
    
	return jsonify({'error': 'Invalid username or password'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
	"""Logout user."""
	logout_user()
	return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/current-user', methods=['GET'])
def current_user_info():
	"""Get current user info."""
	if current_user.is_authenticated:
		return jsonify({
			'authenticated': True,
			'user': {
				'id': current_user.id,
				'username': current_user.username,
				'email': current_user.email
			}
		}), 200
	return jsonify({'authenticated': False}), 200

@app.route('/api/convert', methods=['POST'])
@limiter.limit("30 per hour")
def convert_to_pdf():
	"""Convert uploaded file to PDF."""
	try:
		if 'file' not in request.files:
			return jsonify({'error': 'No file provided'}), 400

		file = request.files['file']
		if file.filename == '':
			return jsonify({'error': 'No file selected'}), 400
        
		if not allowed_file(file.filename):
			return jsonify({'error': f'Unsupported file type. Supported: {", ".join(sorted(ALLOWED_EXTENSIONS))}'}), 400

		filename = secure_filename(file.filename)
		extension = get_file_extension(filename)
		file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		file.save(file_path)

		try:
			# Convert file to PDF
			pdf_io = convert_file_to_pdf(file_path, extension)
			pdf_name = filename.rsplit('.', 1)[0] + '.pdf'

			# Save conversion history if user is logged in
			if current_user.is_authenticated:
				conn = sqlite3.connect(DATABASE)
				c = conn.cursor()
				c.execute('INSERT INTO conversion_history (user_id, filename, file_type) VALUES (?, ?, ?)',
						  (current_user.id, filename, extension))
				conn.commit()
				conn.close()

			# Clean up temp file
			if os.path.exists(file_path):
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
			return jsonify({'error': f'Conversion failed: {str(convert_error)}'}), 500
	except Exception as e:
		return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/api/download-code', methods=['GET'])
@limiter.limit("5 per hour")
def download_code():
	"""Download entire codebase as ZIP."""
	try:
		zip_io = io.BytesIO()
        
		# Files to exclude
		exclude_patterns = [
			'users.db', '.env', '__pycache__', '.git', '.venv', 'venv',
			'node_modules', '.pyc', '.DS_Store', 'test_reports'
		]
        
		with zipfile.ZipFile(zip_io, 'w', zipfile.ZIP_DEFLATED) as zipf:
			for root, dirs, files in os.walk('/app'):
				# Filter out excluded directories
				dirs[:] = [d for d in dirs if not any(ex in d for ex in exclude_patterns)]
                
				for file in files:
					# Skip excluded files
					if any(ex in file for ex in exclude_patterns):
						continue
                    
					file_path = os.path.join(root, file)
					arcname = os.path.relpath(file_path, '/app')
					zipf.write(file_path, arcname)
        
		zip_io.seek(0)
		return send_file(
			zip_io,
			mimetype='application/zip',
			as_attachment=True,
			download_name=f'universal-pdf-converter-{datetime.now().strftime("%Y%m%d")}.zip'
		)
	except Exception as e:
		return jsonify({'error': f'Failed to create ZIP: {str(e)}'}), 500

@app.route('/api/history', methods=['GET'])
@login_required
def conversion_history():
	"""Get user's conversion history."""
	try:
		conn = sqlite3.connect(DATABASE)
		c = conn.cursor()
		c.execute('''
			SELECT filename, file_type, converted_at 
			FROM conversion_history 
			WHERE user_id = ? 
			ORDER BY converted_at DESC 
			LIMIT 50
		''', (current_user.id,))
		history = c.fetchall()
		conn.close()
        
		return jsonify({
			'history': [
				{'filename': h[0], 'type': h[1], 'date': h[2]}
				for h in history
			]
		}), 200
	except Exception as e:
		return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
	"""Health check endpoint."""
	return jsonify({
		'status': 'ok',
		'supported_formats': len(ALLOWED_EXTENSIONS),
		'features': ['multi-format', 'authentication', 'rate-limiting', 'code-download']
	}), 200

@app.errorhandler(413)
def too_large(e):
	"""Handle file too large error."""
	return jsonify({'error': 'File is too large. Maximum size is 100MB'}), 413

@app.errorhandler(429)
def ratelimit_handler(e):
	"""Handle rate limit exceeded."""
	return jsonify({'error': 'Rate limit exceeded. Please try again later.'}), 429

if __name__ == '__main__':
	# Initialize database
	init_db()
    
	port = int(os.environ.get('PORT', 5000))
	app.run(debug=False, host='0.0.0.0', port=port)
# --- END FULL FLASK APP CODE ---

