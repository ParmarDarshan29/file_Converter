#!/bin/bash

# File Converter Setup Script
# This script helps set up the environment for the Jupyter Notebook to PDF Converter

echo "🚀 Jupyter Notebook to PDF Converter - Setup Script"
echo "=================================================="
echo ""

# Check Python version
echo "✓ Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python $PYTHON_VERSION found"
echo ""

# Check if venv exists
if [ -d "venv" ]; then
    echo "✓ Virtual environment already exists"
else
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

echo ""
echo "🔄 Activating virtual environment..."
source venv/bin/activate

echo "✓ Virtual environment activated"
echo ""

# Install/upgrade pip
echo "📦 Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "✓ pip upgraded"
echo ""

# Install requirements
echo "📦 Installing Python dependencies..."
if pip install -r requirements.txt; then
    echo "✓ Python dependencies installed"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""

# Check for pandoc
echo "✓ Checking for pandoc..."
if ! command -v pandoc &> /dev/null; then
    echo "⚠️  Pandoc is not installed (required for PDF generation)"
    echo "   Install with: sudo apt-get install pandoc"
    echo ""
    read -p "Would you like to install pandoc now? (y/n) " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        sudo apt-get update
        sudo apt-get install pandoc -y
        echo "✓ Pandoc installed"
    fi
else
    PANDOC_VERSION=$(pandoc --version | head -1)
    echo "✓ $PANDOC_VERSION found"
fi

echo ""
echo "=================================================="
echo "✅ Setup Complete!"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Run the application: python app.py"
echo "2. Open http://localhost:5000 in your browser"
echo "3. Upload a .ipynb file and convert it to PDF"
echo ""
echo "To deactivate the virtual environment later, run: deactivate"
echo ""
