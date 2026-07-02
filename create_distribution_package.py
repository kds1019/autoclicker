"""
Create distribution package for sharing with friends
Creates a ZIP file with everything needed
"""

import os
import shutil
import zipfile
import platform
from datetime import datetime

def create_distribution_package():
    """Create a ZIP file ready to share"""
    
    print("\n" + "="*60)
    print("FlightSafety Auto-Clicker - Distribution Package Creator")
    print("="*60)
    print()
    
    # Create distribution folder
    dist_folder = "FlightSafety-AutoClicker-Distribution"
    if os.path.exists(dist_folder):
        print(f"🗑️  Removing old distribution folder...")
        shutil.rmtree(dist_folder)
    
    os.makedirs(dist_folder)
    print(f"✅ Created distribution folder: {dist_folder}")
    
    # Files to include
    files_to_copy = [
        "USER_GUIDE.txt",
        "README.md",
        "config.py",
        "requirements.txt",
    ]
    
    # Platform-specific files
    system = platform.system()
    if system == "Windows":
        files_to_copy.extend([
            "INSTALL.bat",
            "START_AUTO_CLICKER.bat",
        ])
    elif system == "Darwin":
        files_to_copy.extend([
            "INSTALL.sh",
            "START_AUTO_CLICKER.sh",
            "MAC_INSTRUCTIONS.md",
        ])
    else:  # Linux
        files_to_copy.extend([
            "INSTALL.sh",
            "START_AUTO_CLICKER.sh",
        ])
    
    # Python files (for advanced users)
    python_files = [
        "auto_clicker.py",
        "auto_clicker_gui.py",
        "create_desktop_shortcut.py",
        "test_audio.py",
    ]
    
    # Copy files
    print("\n📋 Copying files...")
    for file in files_to_copy:
        if os.path.exists(file):
            shutil.copy2(file, dist_folder)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️  {file} not found (skipping)")
    
    # Copy Python files to a subfolder
    python_folder = os.path.join(dist_folder, "source_code")
    os.makedirs(python_folder)
    for file in python_files:
        if os.path.exists(file):
            shutil.copy2(file, python_folder)
    print(f"  ✅ Python source code → source_code/")
    
    # Check for executable
    exe_found = False
    if system == "Windows":
        exe_path = os.path.join("dist", "FlightSafety-AutoClicker.exe")
        if os.path.exists(exe_path):
            shutil.copy2(exe_path, dist_folder)
            print(f"  ✅ FlightSafety-AutoClicker.exe")
            exe_found = True
    elif system == "Darwin":
        app_path = os.path.join("dist", "FlightSafety-AutoClicker.app")
        if os.path.exists(app_path):
            shutil.copytree(app_path, os.path.join(dist_folder, "FlightSafety-AutoClicker.app"))
            print(f"  ✅ FlightSafety-AutoClicker.app")
            exe_found = True
    
    if not exe_found:
        print("\n  ⚠️  No executable found!")
        print("  Run 'python build_executable.py' first to create the .exe/.app")
        print("  For now, creating package with Python files only...")
    
    # Create ZIP file
    timestamp = datetime.now().strftime("%Y%m%d")
    zip_name = f"FlightSafety-AutoClicker-{timestamp}.zip"
    
    print(f"\n📦 Creating ZIP file: {zip_name}")
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(dist_folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, dist_folder)
                zipf.write(file_path, arcname)
                print(f"  ✅ Added: {arcname}")
    
    # Get ZIP size
    zip_size = os.path.getsize(zip_name) / (1024 * 1024)
    
    print("\n" + "="*60)
    print("✅ DISTRIBUTION PACKAGE CREATED!")
    print("="*60)
    print(f"\n📦 File: {zip_name}")
    print(f"📊 Size: {zip_size:.1f} MB")
    print(f"\n🎯 Ready to share!")
    print("\nYou can now:")
    print(f"  1. Email {zip_name} to friends")
    print(f"  2. Upload to Google Drive / Dropbox")
    print(f"  3. Share via USB drive")
    print("\n📧 Use EMAIL_TEMPLATE.txt for email instructions")
    print()
    
    # Cleanup
    print(f"🗑️  Cleaning up temporary folder...")
    shutil.rmtree(dist_folder)
    
    return zip_name

if __name__ == "__main__":
    try:
        zip_file = create_distribution_package()
        print(f"✅ Success! Share {zip_file} with your friends! 🎉\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")

