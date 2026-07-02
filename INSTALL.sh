#!/bin/bash

# FlightSafety Auto-Clicker Installer for Mac/Linux

echo "=========================================="
echo "FlightSafety Auto-Clicker Installer"
echo "=========================================="
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python 3 is not installed!"
    echo ""
    echo "Please install Python 3 from:"
    echo "https://www.python.org/downloads/"
    echo ""
    echo "Or install via Homebrew:"
    echo "  brew install python3"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ ERROR: pip3 is not installed!"
    echo ""
    echo "Install pip3 with:"
    echo "  python3 -m ensurepip --upgrade"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ pip3 found: $(pip3 --version)"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo ""
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✅ Installation Complete!"
    echo "=========================================="
    echo ""
    echo "To run the auto-clicker:"
    echo "  1. Double-click 'START_AUTO_CLICKER.sh'"
    echo "  OR"
    echo "  2. Run: ./START_AUTO_CLICKER.sh"
    echo "  OR"
    echo "  3. Run: python3 auto_clicker_gui.py"
    echo ""
    
    # Make the launcher executable
    chmod +x START_AUTO_CLICKER.sh
    echo "✅ Made START_AUTO_CLICKER.sh executable"
    echo ""
else
    echo ""
    echo "❌ Installation failed!"
    echo "Please check the error messages above."
    echo ""
fi

read -p "Press Enter to exit..."

