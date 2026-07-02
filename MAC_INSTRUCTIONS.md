# 🍎 Mac Installation & Usage Guide

## 📋 Prerequisites

1. **Python 3** - Check if installed:
   ```bash
   python3 --version
   ```
   
   If not installed:
   - **Option 1:** Install via Homebrew: `brew install python3`
   - **Option 2:** Download from https://www.python.org/downloads/

2. **Google Chrome** - Download from https://www.google.com/chrome/

---

## 🚀 Quick Install

### **Method 1: Double-Click Installer** ⭐ **EASIEST**

1. Right-click `INSTALL.sh` → **Open With** → **Terminal**
2. Wait for installation to complete
3. Right-click `START_AUTO_CLICKER.sh` → **Open With** → **Terminal**

---

### **Method 2: Terminal Commands**

1. Open **Terminal** (Cmd+Space, type "Terminal")
2. Navigate to this folder:
   ```bash
   cd /path/to/flightsafety-auto-clicker
   ```
3. Make scripts executable:
   ```bash
   chmod +x INSTALL.sh START_AUTO_CLICKER.sh
   ```
4. Run installer:
   ```bash
   ./INSTALL.sh
   ```
5. Run the app:
   ```bash
   ./START_AUTO_CLICKER.sh
   ```

---

## 🎮 How to Use

1. **Launch the app** (double-click `START_AUTO_CLICKER.sh`)
2. **Click "LAUNCH BROWSER"** - Chrome opens automatically
3. **Login to FlightSafety** in the browser window
4. **Click "LAUNCH" or "VIEW COURSE"** to start your training
5. **Click "START AUTO-CLICKING"** in the app
6. **Relax!** The app will:
   - Auto-click "Next" buttons
   - Beep when questions appear (you'll hear the "Ping" sound)
   - Pause for you to answer
   - Resume automatically

---

## 🐛 Troubleshooting

### **"Permission denied" error**

Run this in Terminal:
```bash
chmod +x INSTALL.sh START_AUTO_CLICKER.sh
```

### **"python3: command not found"**

Install Python 3:
```bash
brew install python3
```

Or download from: https://www.python.org/downloads/

### **"pip3: command not found"**

Install pip:
```bash
python3 -m ensurepip --upgrade
```

### **Can't hear beeps**

- Check system volume (should be turned up)
- The app uses the system "Ping" sound
- Test it: Run `afplay /System/Library/Sounds/Ping.aiff` in Terminal

### **Chrome doesn't open**

- Make sure Chrome is installed
- Download from: https://www.google.com/chrome/

---

## 💡 Tips

- **Keep Terminal window open** while the app is running
- **Don't close Chrome** while auto-clicking
- **Stay nearby** - you need to answer questions when they appear
- **Adjust delays** in `config.py` if clicks are too fast/slow

---

## 🔧 Advanced: Run Without GUI

If you prefer command-line only:

```bash
python3 auto_clicker.py
```

---

**Enjoy your automated training! ✈️**

