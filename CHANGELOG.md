# Changelog

## Version 2.0 - Cross-Platform Support (2026-01-28)

### ✨ New Features

- **🍎 Mac Support** - Now works on macOS!
- **🐧 Linux Support** - Works on Linux too!
- **🔊 Cross-Platform Audio** - Beeps work on all operating systems:
  - Windows: Uses `winsound.Beep()`
  - Mac: Uses system "Ping" sound via `afplay`
  - Linux: Uses `beep` command
- **📦 Easy Installers** - One-click installation:
  - `INSTALL.bat` for Windows
  - `INSTALL.sh` for Mac/Linux
- **🚀 Easy Launchers** - Simple startup scripts:
  - `START_AUTO_CLICKER.bat` for Windows
  - `START_AUTO_CLICKER.sh` for Mac/Linux

### 🔧 Technical Changes

- Replaced Windows-only `winsound` import with cross-platform solution
- Added `platform.system()` detection for OS-specific features
- Updated `play_alert()` function to work on all platforms
- Browser automation already cross-platform (thanks to Selenium + webdriver-manager)

### 📝 Documentation

- Updated `README.md` with Mac/Linux instructions
- Added `MAC_INSTRUCTIONS.md` for Mac-specific setup
- Added `CHANGELOG.md` (this file)
- Updated troubleshooting section for all platforms

### 🗂️ New Files

- `INSTALL.sh` - Mac/Linux installer script
- `INSTALL.bat` - Windows installer script (improved)
- `START_AUTO_CLICKER.sh` - Mac/Linux launcher
- `MAC_INSTRUCTIONS.md` - Mac-specific guide
- `CHANGELOG.md` - Version history

### 🐛 Bug Fixes

- Fixed audio alerts to work on non-Windows systems
- Improved error messages for missing dependencies

---

## Version 1.0 - Initial Release

### Features

- Auto-click "Next" buttons in FlightSafety training
- Detect questions via "Submit" button
- Alert user with beeps when questions appear
- Random delays (1-20 seconds) to appear human
- GUI interface for easy use
- Auto-mute course audio
- Windows support only

