#!/bin/bash

# FlightSafety Auto-Clicker Launcher for Mac/Linux
# This script launches the auto-clicker GUI

echo "=========================================="
echo "FlightSafety Auto-Clicker"
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
    read -p "Press Enter to exit..."
    exit 1
fi

echo "✅ Python 3 found: $(python3 --version)"
echo ""

# Check if dependencies are installed
echo "🔍 Checking dependencies..."
if ! python3 -c "import selenium" 2>/dev/null; then
    echo "⚠️  Dependencies not installed. Installing now..."
    echo ""
    pip3 install -r requirements.txt
    echo ""
fi

echo "🚀 Starting Auto-Clicker GUI..."
echo ""

# Launch the GUI
python3 auto_clicker_gui.py

echo ""
echo "=========================================="
echo "Auto-Clicker closed"
echo "=========================================="

