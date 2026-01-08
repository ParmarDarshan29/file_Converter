# Getting Started Checklist ✅

## Pre-Setup (System Level)

- [ ] Verify Python 3.8+ is installed
  ```bash
  python3 --version
  ```

- [ ] Install pip if not available
  ```bash
  sudo apt-get install python3-pip
  ```

- [ ] Install pandoc (required for PDF generation)
  ```bash
  sudo apt-get update
  sudo apt-get install pandoc
  ```

## Setup Phase

### Option A: Automated Setup (Recommended)

- [ ] Run setup script
  ```bash
  chmod +x setup.sh
  ./setup.sh
  ```

- [ ] Skip to "Running the Application"

### Option B: Manual Setup

- [ ] Create virtual environment
  ```bash
  python3 -m venv venv
  ```

- [ ] Activate virtual environment
  ```bash
  source venv/bin/activate
  ```

- [ ] Install Python dependencies
  ```bash
  pip install -r requirements.txt
  ```

## Configuration

- [ ] Review configuration options (optional)
  ```bash
  cp .env.example .env
  ```

- [ ] Edit `.env` if needed (default settings work fine)

## Running the Application

- [ ] Ensure virtual environment is activated
  ```bash
  source venv/bin/activate
  ```

- [ ] Start the Flask application
  ```bash
  python app.py
  ```

- [ ] Verify app is running
  - Look for message: `Running on http://127.0.0.1:5000`

## Testing the Application

- [ ] Open web browser
- [ ] Navigate to: http://localhost:5000
- [ ] Verify UI loads properly (purple/blue gradient)
- [ ] Check that upload area is visible

### Test Conversion

- [ ] Drag sample_notebook.ipynb to upload area
  ```
  Sample file location: ./sample_notebook.ipynb
  ```

- [ ] Click "Convert to PDF" button
- [ ] Wait for conversion to complete
- [ ] Verify PDF downloads automatically
- [ ] Check PDF opens and displays correctly

## Alternative Testing (Command Line)

- [ ] Test API endpoint directly
  ```bash
  curl -X POST -F "file=@sample_notebook.ipynb" \
    http://localhost:5000/api/convert -o test_output.pdf
  ```

- [ ] Verify PDF was created
  ```bash
  ls -lh test_output.pdf
  ```

## Verification

- [ ] Web interface loads without errors ✅
- [ ] Drag-and-drop area is visible ✅
- [ ] File upload works ✅
- [ ] Conversion completes successfully ✅
- [ ] PDF downloads correctly ✅
- [ ] Converted PDF opens properly ✅

## Documentation Review

- [ ] Read QUICK_START.md for quick reference
- [ ] Review README.md for detailed information
- [ ] Check SETUP.md for troubleshooting

## Troubleshooting Checklist

If something doesn't work:

- [ ] Virtual environment is activated?
  ```bash
  source venv/bin/activate
  ```

- [ ] All dependencies installed?
  ```bash
  pip install -r requirements.txt
  ```

- [ ] Pandoc installed?
  ```bash
  which pandoc
  ```

- [ ] Port 5000 is available?
  ```bash
  lsof -i :5000
  ```

- [ ] No syntax errors in code?
  ```bash
  python -m py_compile app.py
  ```

- [ ] Flask running properly?
  - Check console output for errors
  - Verify Flask version: `pip show Flask`

## Common Issues & Solutions

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `pandoc not found` | Run `sudo apt-get install pandoc` |
| `Port 5000 in use` | Kill process: `lsof -ti :5000 \| xargs kill -9` |
| `Permission denied setup.sh` | Run `chmod +x setup.sh` first |
| Browser shows connection error | Ensure app.py is running |

## First Upload Tips

- [ ] Start with sample_notebook.ipynb
- [ ] File should be max 50MB
- [ ] Only .ipynb files are supported
- [ ] Wait for progress bar to complete
- [ ] PDF should download automatically

## Deactivate When Done

```bash
deactivate
```

## Next Steps After Verification

- [ ] Customize the application (optional)
- [ ] Commit to git if needed
- [ ] Share with team/users
- [ ] Monitor usage and performance
- [ ] Plan future enhancements

## Optional Customizations

- [ ] Change the port number in app.py
- [ ] Modify UI styling in templates/index.html
- [ ] Update max file size in app.py
- [ ] Add custom error messages
- [ ] Create custom PDF styling

## Maintenance

- [ ] Keep dependencies updated
  ```bash
  pip install --upgrade -r requirements.txt
  ```

- [ ] Monitor for security updates
- [ ] Clean up temp files periodically
- [ ] Review error logs

## Success! 🎉

Once all checkboxes are complete, your Jupyter Notebook to PDF Converter is:

✅ Installed
✅ Configured
✅ Running
✅ Tested
✅ Ready for use!

Enjoy converting notebooks to PDFs! 📓➜📄
