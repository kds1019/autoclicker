"""
Create a desktop shortcut for the FlightSafety Auto-Clicker
"""
import os
import winshell
from win32com.client import Dispatch

# Get the desktop path
desktop = winshell.desktop()

# Get the current directory (where the batch file is)
current_dir = os.path.dirname(os.path.abspath(__file__))
batch_file = os.path.join(current_dir, "START_AUTO_CLICKER.bat")

# Create shortcut path
shortcut_path = os.path.join(desktop, "FlightSafety Auto-Clicker.lnk")

# Create the shortcut
shell = Dispatch('WScript.Shell')
shortcut = shell.CreateShortCut(shortcut_path)
shortcut.Targetpath = batch_file
shortcut.WorkingDirectory = current_dir
shortcut.IconLocation = batch_file
shortcut.Description = "FlightSafety Auto-Clicker - Auto-click through training slides"
shortcut.save()

print("✅ Desktop shortcut created successfully!")
print(f"📍 Location: {shortcut_path}")
print("\n🚀 You can now double-click 'FlightSafety Auto-Clicker' on your desktop to start!")
input("\nPress ENTER to close...")

