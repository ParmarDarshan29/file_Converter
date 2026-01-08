# Quick Start Guide

## 1. Install Dependencies

### System Level (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install python3-pip pandoc
```

### Python Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python packages
pip install -r requirements.txt
```

## 2. Run the Application

```bash
python app.py
```

The application will be available at: **http://localhost:5000**

## 3. How to Use

1. **Open the web interface** - Go to http://localhost:5000
2. **Upload a notebook** - Click or drag your `.ipynb` file
3. **Convert** - Click the "Convert to PDF" button
4. **Download** - The PDF will automatically download

## 4. Project Structure

```
file_Converter/
├── app.py                    # Flask backend
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables example
├── .gitignore                # Git ignore rules
├── README.md                 # Full documentation
├── SETUP.md                  # This file
└── templates/
    └── index.html            # Web interface
```

## 5. Configuration

Copy `.env.example` to `.env` and modify as needed:
```bash
cp .env.example .env
```

## 6. API Endpoints

### Convert Notebook to PDF
```bash
curl -X POST -F "file=@notebook.ipynb" http://localhost:5000/api/convert -o output.pdf
```

### Health Check
```bash
curl http://localhost:5000/api/health
```

## 7. Troubleshooting

**Error: pandoc not found**
- Install pandoc: `sudo apt-get install pandoc`

**Error: ModuleNotFoundError**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Port 5000 already in use**
- Change port in `app.py` or kill existing process:
  ```bash
  lsof -ti :5000 | xargs kill -9
  ```

## 8. Deactivate Virtual Environment

```bash
deactivate
```

## Features

✅ Drag-and-drop upload
✅ Real-time progress tracking
✅ Secure file handling
✅ Beautiful, responsive UI
✅ Support for large files (up to 50MB)
✅ Works with all notebook content
