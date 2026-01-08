# Quick Reference Card

## 🚀 Start the Project (3 Steps)

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install dependencies (first time only)
pip install -r requirements.txt

# 3. Run the app
python app.py
```

Visit: http://localhost:5000

---

## 📋 System Requirements

- Python 3.8+
- pandoc (for PDF generation)
- 50MB disk space

### Install System Dependencies
```bash
sudo apt-get update
sudo apt-get install python3-pip pandoc
```

---

## 🔧 First-Time Setup

**Option 1: Automated (Recommended)**
```bash
chmod +x setup.sh
./setup.sh
```

**Option 2: Manual**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
sudo apt-get install pandoc
```

---

## 📁 Project Structure

```
file_Converter/
├── app.py                     # Backend (Flask)
├── templates/index.html       # Frontend (Web UI)
├── requirements.txt           # Dependencies
├── sample_notebook.ipynb      # Test file
├── setup.sh                   # Automated setup
├── README.md                  # Full docs
├── SETUP.md                   # Setup guide
└── PROJECT_SUMMARY.md         # Project info
```

---

## 🌐 API Endpoints

| Method | URL | Purpose |
|--------|-----|---------|
| GET | `/` | Web interface |
| POST | `/api/convert` | Convert notebook |
| GET | `/api/health` | Status check |

### Example: Convert via Command Line
```bash
curl -X POST -F "file=@notebook.ipynb" \
  http://localhost:5000/api/convert -o output.pdf
```

---

## 🎨 Frontend Features

✅ Drag & drop upload
✅ Real-time progress
✅ Error messages
✅ Success notifications
✅ Mobile responsive
✅ Modern UI

---

## 🔒 Security

- Only .ipynb files allowed
- Max file size: 50MB
- Secure filename handling
- Auto cleanup of temp files
- CORS enabled

---

## ⚙️ Configuration

### Change Port
Edit `app.py`, line with `port=5000`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
```

### Environment Variables
Create `.env` file:
```
FLASK_ENV=development
FLASK_DEBUG=True
```

---

## 🐛 Common Issues

| Problem | Solution |
|---------|----------|
| `pandoc not found` | `sudo apt-get install pandoc` |
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| `Port 5000 in use` | `lsof -ti :5000 \| xargs kill -9` |
| No virtual env | `python3 -m venv venv` |

---

## 📊 File Limits

| Property | Limit |
|----------|-------|
| Max file size | 50 MB |
| Allowed format | .ipynb only |
| Concurrent uploads | No limit |

---

## 🧪 Testing

### Test with Sample File
```bash
# From browser: Upload sample_notebook.ipynb
# Or via CLI:
curl -X POST -F "file=@sample_notebook.ipynb" \
  http://localhost:5000/api/convert -o test_output.pdf
```

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README.md | Complete documentation |
| SETUP.md | Installation guide |
| PROJECT_SUMMARY.md | Project overview |
| .env.example | Config template |

---

## 🛑 Stop the Application

Press `Ctrl + C` in the terminal

---

## 🔄 Deactivate Virtual Environment

```bash
deactivate
```

---

## 💡 Tips

1. **First time setup?** Run `./setup.sh`
2. **Need to change port?** Edit `app.py`
3. **Check if working?** Visit http://localhost:5000/api/health
4. **Test conversion?** Use `sample_notebook.ipynb`
5. **See logs?** Check terminal output while running

---

## 📞 Quick Help

```bash
# Activate venv
source venv/bin/activate

# Run app
python app.py

# Install deps
pip install -r requirements.txt

# Check health
curl http://localhost:5000/api/health

# Exit app
Ctrl + C

# Exit venv
deactivate
```

---

**Version:** 1.0.0 | **Last Updated:** January 2026
