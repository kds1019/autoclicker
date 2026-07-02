"""
Test script to verify cross-platform audio works
Run this to test if beeps work on your system
"""

import os
import platform
import time

def test_audio():
    """Test audio on current platform"""
    system = platform.system()
    
    print("=" * 50)
    print("FlightSafety Auto-Clicker - Audio Test")
    print("=" * 50)
    print(f"\n🖥️  Detected OS: {system}")
    print(f"📊 Platform: {platform.platform()}")
    print(f"🐍 Python: {platform.python_version()}")
    print("\n🔊 Testing audio alert...")
    print("You should hear 3 beeps...\n")
    
    for i in range(3):
        print(f"Beep {i+1}/3...")
        
        if system == "Darwin":  # macOS
            print("  → Using macOS 'Ping' sound")
            os.system('afplay /System/Library/Sounds/Ping.aiff')
        elif system == "Windows":
            print("  → Using Windows beep")
            try:
                import winsound
                winsound.Beep(1000, 500)  # 1000 Hz, 500ms
            except ImportError:
                print("  ⚠️  winsound not available (not on Windows?)")
        else:  # Linux
            print("  → Using Linux beep command")
            os.system('beep -f 1000 -l 500')
        
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("✅ Audio test complete!")
    print("=" * 50)
    print("\nDid you hear 3 beeps?")
    print("  - YES: Audio is working! ✅")
    print("  - NO: Check your system volume 🔊")
    print("\nIf you didn't hear anything:")
    
    if system == "Darwin":
        print("  Mac: Make sure volume is up")
        print("  Try: System Preferences → Sound → Output")
    elif system == "Windows":
        print("  Windows: Make sure volume is up")
        print("  Try: Volume mixer in taskbar")
    else:
        print("  Linux: Install beep package")
        print("  Try: sudo apt-get install beep")
    
    print("\n")

if __name__ == "__main__":
    test_audio()

