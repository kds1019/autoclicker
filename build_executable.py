"""
Build standalone executable for FlightSafety Auto-Clicker
Creates a single .exe (Windows) or .app (Mac) file that friends can just double-click

Usage:
    python build_executable.py
"""

import os
import sys
import platform
import subprocess

def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✅ PyInstaller found")
        return True
    except ImportError:
        print("❌ PyInstaller not installed")
        print("\n📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✅ PyInstaller installed!")
        return True

def build_executable():
    """Build the executable"""
    system = platform.system()
    
    print("\n" + "="*60)
    print("FlightSafety Auto-Clicker - Executable Builder")
    print("="*60)
    print(f"\n🖥️  Building for: {system}")
    print(f"📊 Platform: {platform.platform()}")
    print(f"🐍 Python: {platform.python_version()}\n")
    
    # Check PyInstaller
    if not check_pyinstaller():
        print("❌ Failed to install PyInstaller")
        return False
    
    # Build command
    print("\n🔨 Building executable...")
    print("This may take 2-5 minutes...\n")
    
    # PyInstaller options
    options = [
        "pyinstaller",
        "--onefile",                    # Single file
        "--windowed",                   # No console window (GUI only)
        "--name=FlightSafety-AutoClicker",  # Output name
        "--clean",                      # Clean cache
        "--noconfirm",                  # Overwrite without asking
    ]
    
    # Add icon if available
    if system == "Windows" and os.path.exists("icon.ico"):
        options.append("--icon=icon.ico")
    elif system == "Darwin" and os.path.exists("icon.icns"):
        options.append("--icon=icon.icns")
    
    # Add hidden imports (dependencies that PyInstaller might miss)
    options.extend([
        "--hidden-import=selenium",
        "--hidden-import=webdriver_manager",
        "--hidden-import=selenium.webdriver.chrome.service",
        "--hidden-import=selenium.webdriver.common.by",
    ])
    
    # Main file
    options.append("auto_clicker_gui.py")
    
    # Run PyInstaller
    try:
        result = subprocess.run(options, check=True)
        
        print("\n" + "="*60)
        print("✅ BUILD SUCCESSFUL!")
        print("="*60)
        
        # Find the executable
        if system == "Windows":
            exe_path = os.path.join("dist", "FlightSafety-AutoClicker.exe")
            print(f"\n📦 Executable created: {exe_path}")
            print(f"📊 Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
            print("\n🎯 To share with friends:")
            print(f"   1. Send them: {exe_path}")
            print("   2. They double-click it")
            print("   3. Done! ✅")
        elif system == "Darwin":
            app_path = os.path.join("dist", "FlightSafety-AutoClicker.app")
            print(f"\n📦 Application created: {app_path}")
            print("\n🎯 To share with friends:")
            print(f"   1. Compress {app_path} to ZIP")
            print("   2. Send them the ZIP file")
            print("   3. They extract and double-click")
            print("   4. Done! ✅")
        else:
            exe_path = os.path.join("dist", "FlightSafety-AutoClicker")
            print(f"\n📦 Executable created: {exe_path}")
        
        print("\n⚠️  NOTE: Windows might show 'Unknown Publisher' warning")
        print("    Friends should click 'More info' → 'Run anyway'")
        print("    (This is normal for unsigned executables)")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    print("\n🚀 Starting build process...\n")
    
    if build_executable():
        print("\n✅ All done! Your executable is ready to share! 🎉\n")
    else:
        print("\n❌ Build failed. Please check the errors above.\n")

