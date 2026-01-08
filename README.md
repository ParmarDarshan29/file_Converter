# Jupyter Notebook to PDF Converter

A simple, fast, and user-friendly web application that converts Jupyter Notebook (.ipynb) files to PDF format.

## Features

- 📁 Drag-and-drop file upload
- ⚡ Fast conversion
- 🔒 Secure processing
- 📊 Support for all notebook content (code, markdown, outputs)
- 💾 Up to 50MB file size support
- 🎨 Modern, responsive UI

## Tech Stack

### Backend
- **Flask**: Lightweight web framework
- **nbconvert**: Jupyter notebook conversion library
- **Python**: Core language

### Frontend
- **HTML5**: Structure
- **CSS3**: Styling with gradient design
- **Vanilla JavaScript**: Dynamic interactions

## Installation

### Prerequisites
- Python 3.8+
- pip
- pandoc (required for PDF generation)

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd file_Converter
   ```

2. **Install system dependency (pandoc)**
   ```bash
   # On Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install pandoc

   # On macOS
   brew install pandoc

   # On Windows
   # Download from https://github.com/jgm/pandoc/releases
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the application

```bash
python app.py
```

The application will start on `http://localhost:5000`

### Converting a notebook

1. Open the web interface in your browser
2. Click or drag your `.ipynb` file to the upload area
3. Click "Convert to PDF"
4. The PDF will automatically download when ready

## API Endpoints

### `GET /`
Serves the main web interface

### `POST /api/convert`
Converts an uploaded IPYNB file to PDF

**Request:**
- Content-Type: multipart/form-data
- Parameter: `file` (required, .ipynb file)

**Response:**
- Success: Returns PDF file (application/pdf)
- Error: JSON with error message

**Example:**
```bash
curl -X POST -F "file=@notebook.ipynb" http://localhost:5000/api/convert -o output.pdf
```

### `GET /api/health`
Health check endpoint

**Response:**
```json
{"status": "ok"}
```

## Configuration

Environment variables (optional):
- `FLASK_ENV`: Set to `development` or `production`
- `FLASK_DEBUG`: Set to `True` for debug mode

Create a `.env` file:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

## Limitations

- Maximum file size: 50MB
- Only `.ipynb` files are supported
- Requires pandoc for PDF generation

## Troubleshooting

### Pandoc not found error
Ensure pandoc is installed on your system. Follow the installation steps above.

### ModuleNotFoundError
Make sure you're in the virtual environment and all dependencies are installed:
```bash
pip install -r requirements.txt
```

### Port already in use
Change the port in `app.py` or kill the process using port 5000:
```bash
# On Linux/macOS
lsof -ti :5000 | xargs kill -9

# On Windows
netstat -ano | findstr :5000
```

## File Structure

```
file_Converter/
├── app.py                  # Flask application
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Web interface
├── README.md              # Documentation
└── .env                   # Environment variables (optional)
```

## Future Enhancements

- [ ] Batch file conversion
- [ ] Custom PDF styling options
- [ ] File conversion history
- [ ] Email PDF delivery
- [ ] Support for other formats (HTML, DOCX)
- [ ] Progress tracking for large files
- [ ] User authentication

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Open an issue on GitHub
3. Contact the maintainer

## Acknowledgments

- [nbconvert](https://nbconvert.readthedocs.io/) - Jupyter Notebook conversion
- [Flask](https://flask.palletsprojects.com/) - Web framework
- [Pandoc](https://pandoc.org/) - Document converter