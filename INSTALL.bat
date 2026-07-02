@echo off
REM FlightSafety Auto-Clicker Installer for Windows

REM Always run from the folder this script lives in
cd /d "%~dp0"

echo ==========================================
echo FlightSafety Auto-Clicker Installer
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo.
    echo Please install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)

echo Python found:
python --version
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: pip is not installed!
    echo.
    echo Install pip with:
    echo   python -m ensurepip --upgrade
    echo.
    pause
    exit /b 1
)

echo pip found:
pip --version
echo.

REM Install dependencies
echo Installing dependencies...
echo.
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ERROR: Installation failed!
    echo Please check the error messages above.
    echo.
    pause
    exit /b 1
)

echo.
echo ==========================================
echo Installation Complete!
echo ==========================================
echo.
echo To run the auto-clicker:
echo   1. Double-click 'START_AUTO_CLICKER.bat'
echo   OR
echo   2. Run: python auto_clicker_gui.py
echo.
echo Creating desktop shortcut...
python create_desktop_shortcut.py

echo.
pause

