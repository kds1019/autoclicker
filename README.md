# Training Auto-Clicker 🚁

Automatically clicks through online training slides and alerts you when questions appear.

**✅ Works with FlightSafety and CtSys online training**
**✅ Works on Windows, Mac, and Linux!**

---

## ✨ Features

- ✅ **Auto-clicks "Next" buttons** with random 1-20 second delays (looks human!)
- ✅ **Detects questions** by looking for "Submit" buttons
- ✅ **Loud beep alert** when questions appear (cross-platform audio)
- ✅ **Pauses automatically** when questions detected
- ✅ **Resumes clicking** after you answer
- ✅ **Easy-to-use GUI** - No command line needed!
- ✅ **Cross-platform** - Windows, Mac, Linux

---

## 🚀 Quick Start

### **Option 1: Easy Install (Recommended)** ⭐

#### **Windows:**
1. Double-click `INSTALL.bat`
2. Wait for installation to complete
3. Double-click `START_AUTO_CLICKER.bat` (or use desktop shortcut)

#### **Mac/Linux:**
1. Open Terminal in this folder
2. Run: `chmod +x INSTALL.sh && ./INSTALL.sh`
3. Run: `./START_AUTO_CLICKER.sh`

---

### **Option 2: Manual Install**

#### **Windows:**

Open Command Prompt in this folder and run:

```bash
pip install -r requirements.txt
python auto_clicker_gui.py
```

#### **Mac/Linux:**

Open Terminal in this folder and run:

```bash
pip3 install -r requirements.txt
python3 auto_clicker_gui.py
```

---

## 🎮 How to Use

### **Using the GUI:**

1. 🚀 **Click "LAUNCH BROWSER"** - Chrome opens automatically
2. 🔐 **Login to your training site** in the browser
3. 📚 **Click "LAUNCH" or "VIEW COURSE"** to start your course
4. ▶️ **Click "START AUTO-CLICKING"** in the GUI
5. ☕ **Relax!** The app will:
   - Auto-click "Next" buttons every 1-20 seconds (random)
   - Beep loudly when questions appear (5 beeps)
   - Pause automatically for you to answer
   - Resume clicking after you submit your answer

### **Controls:**

- **STOP button** - Stop the auto-clicker
- **Close browser manually** when done (browser stays open)

---

## ⚙️ Configuration

Edit `config.py` to customize:

- **Training system** - Set `TRAINING_SITE` to `"flightsafety"` or `"ctsys"` to
  choose which site the browser opens. Add your own site under `TRAINING_SITES`
  (name, url, content_frame) to support another training portal.
- **Click delay range** - Change `MIN_CLICK_DELAY` and `MAX_CLICK_DELAY`
- **Beep settings** - Change `BEEP_COUNT`, `BEEP_FREQUENCY`, `BEEP_DURATION`
- **Button keywords** - Add more keywords if buttons aren't detected

---

## 🐛 Troubleshooting

### **"Python is not installed" (Windows)**

- Download Python from https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation!

### **"Python is not installed" (Mac)**

- Install via Homebrew: `brew install python3`
- Or download from https://www.python.org/downloads/

### **"Could not launch Chrome"**

- Make sure Chrome is installed
- Run the installer script again: `INSTALL.bat` (Windows) or `./INSTALL.sh` (Mac)

### **"Next button not found"**

- The button might have different text
- Edit `config.py` and add the button text to `NEXT_BUTTON_KEYWORDS`

### **Questions not detected**

- Edit `config.py` and add keywords to `SUBMIT_BUTTON_KEYWORDS`

### **No sound on Mac**

- Make sure system volume is turned up
- The app uses the system "Ping" sound

### **Permission denied on Mac**

- Run: `chmod +x START_AUTO_CLICKER.sh`
- Then: `./START_AUTO_CLICKER.sh`

---

## 📝 Notes

- **Don't close the Chrome window** while the script is running
- **The script won't close your browser** when it stops (close manually when done)
- **You can run this every year** for your training!
- **Works on Windows, Mac, and Linux** - share with friends!

---

## 🎯 Tips

- **Test it first** on a practice course to make sure it works
- **Stay nearby** when running - you need to answer questions
- **Adjust delays** in `config.py` if clicks are too fast/slow

---

**Enjoy your automated training! ✈️**

