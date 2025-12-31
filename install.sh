#!/bin/bash
# Vibecode Studio Installation Script (Linux/Mac)

echo "╔════════════════════════════════════════╗"
echo "║   Vibecode Studio Installation        ║"
echo "║   Your AI Development Team in a Box    ║"
echo "╚════════════════════════════════════════╝"
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $python_version"

# Check if Python 3.8+
if ! python3 -c 'import sys; exit(0 if sys.version_info >= (3, 8) else 1)'; then
    echo "❌ Error: Python 3.8 or higher required"
    exit 1
fi

echo "✅ Python version OK"
echo ""

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "❌ Failed to create virtual environment"
    exit 1
fi

echo "✅ Virtual environment created"
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo "✅ Dependencies installed"
echo ""

# Create .vibecode directory if it doesn't exist
if [ ! -d ".vibecode" ]; then
    echo "Creating .vibecode directory..."
    mkdir .vibecode
    mkdir .vibecode/sessions
    echo "✅ .vibecode directory created"
fi

echo ""
echo "╔════════════════════════════════════════╗"
echo "║   Installation Complete! 🎉            ║"
echo "╚════════════════════════════════════════╝"
echo ""
echo "To start Vibecode Studio:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run: python vibecode_studio.py"
echo ""
echo "Or use the quick start:"
echo "  ./run.sh"
echo ""
