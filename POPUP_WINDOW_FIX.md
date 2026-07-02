# Popup Window Support Improvements

## Problem
The auto-clicker wasn't working properly with courses that open in a **new popup window** (as opposed to a new tab).

## Changes Made

### 1. **Improved Window Detection** (`auto_clicker.py`)
- Added better debugging output to show all windows/tabs
- Increased wait times for popup windows to fully load (2-3 seconds)
- Added window title display when switching windows

### 2. **Enhanced Button Detection**
- Added support for `<div>` elements with `onclick` handlers (common in popup windows)
- Added checks for multiple common button IDs:
  - `btnNext` (already existed)
  - `nextButton`
  - `btnContinue`
  - `next-button`
  - `continueButton`
- Improved frame detection to try all iframes, not just "sco" frame

### 3. **Better Debugging**
- Added current URL display when switching to popup window mode
- More detailed logging of frame detection
- Shows which window is active at each step

## How to Test

### Option 1: Use the Debug Script
1. Run the test script:
   ```bash
   python test_popup_window.py
   ```
2. Follow the prompts to login and launch your course
3. The script will show detailed information about:
   - How many windows are detected
   - Window titles and URLs
   - Frames found
   - Whether Next button can be found

### Option 2: Use the GUI (Normal Usage)
1. Run the auto-clicker GUI:
   ```bash
   python auto_clicker_gui.py
   ```
   Or double-click `START_AUTO_CLICKER.bat`

2. Click "LAUNCH BROWSER"
3. Login to FlightSafety
4. Click "LAUNCH" or "VIEW COURSE" to open your course in a popup window
5. Click "START AUTO-CLICKING"
6. **Watch the console output** - it will now show:
   - "No 'sco' frame found - this appears to be a popup window course"
   - Current URL
   - Frames detected
   - Buttons found

## What to Look For

### If it's working:
- You'll see: `✅ Clicked Next (on main page)` or `✅ Clicked Next (in frame: ...)`
- The course will advance automatically

### If it's still not working:
Look at the console output and check:
1. **How many windows detected?** Should be 2+ (main window + popup)
2. **Current URL?** Should be the course URL, not the login page
3. **Frames found?** Shows how many iframes exist
4. **Buttons found?** Shows what clickable elements were detected

## Next Steps if Still Not Working

If the auto-clicker still doesn't work with your popup window course, please:

1. Run `test_popup_window.py` and share the output
2. Take a screenshot of the course window
3. Right-click on the "Next" button and select "Inspect Element" to see:
   - What HTML tag it is (`<button>`, `<div>`, `<a>`, etc.)
   - What `id` or `class` it has
   - If it has an `onclick` handler

With this information, I can add specific support for your course's button type.

## Technical Details

The auto-clicker now handles three types of course layouts:

1. **Tab-based with "sco" frame** (original support)
   - Course opens in a new tab
   - Content is inside an iframe named "sco"

2. **Popup window with frames** (improved support)
   - Course opens in a popup window
   - Content is inside unnamed iframes
   - Auto-clicker now tries all frames

3. **Popup window without frames** (new support)
   - Course opens in a popup window
   - Content is directly on the page
   - Buttons might be `<div>` elements with onclick handlers
   - Auto-clicker now checks for div#btnNext and other common IDs

