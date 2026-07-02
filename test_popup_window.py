"""
Test script to debug popup window detection
Run this to see what windows/frames are detected
"""
from auto_clicker import TrainingAutoClicker
import time

print("="*60)
print("POPUP WINDOW DEBUGGER")
print("="*60)

# Create clicker instance
clicker = TrainingAutoClicker(gui_mode=False)

# Launch browser
print("\n1. Launching browser...")
if not clicker.setup_browser():
    print("❌ Failed to launch browser")
    exit(1)

print("\n2. Please:")
print("   - Login to FlightSafety")
print("   - Click LAUNCH/VIEW COURSE to open your course")
print("   - Wait for the course window/tab to open")
input("\nPress ENTER when course is open...")

# Check windows
print("\n3. Checking windows...")
all_windows = clicker.driver.window_handles
print(f"   Found {len(all_windows)} windows/tabs")

for i, window_handle in enumerate(all_windows):
    clicker.driver.switch_to.window(window_handle)
    print(f"\n   Window {i+1}:")
    print(f"      Title: {clicker.driver.title}")
    print(f"      URL: {clicker.driver.current_url}")

# Switch to last window (course)
if len(all_windows) > 1:
    clicker.driver.switch_to.window(all_windows[-1])
    print(f"\n4. Switched to course window: '{clicker.driver.title}'")
else:
    print(f"\n4. Only one window found - using it")

# Check for frames
print("\n5. Checking for frames...")
try:
    frames = clicker.driver.find_elements("tag name", "frame")
    iframes = clicker.driver.find_elements("tag name", "iframe")
    print(f"   Found {len(frames)} <frame> and {len(iframes)} <iframe> elements")
    
    if iframes:
        for i, iframe in enumerate(iframes):
            iframe_id = iframe.get_attribute("id") or "(no id)"
            iframe_name = iframe.get_attribute("name") or "(no name)"
            print(f"      iframe {i+1}: id='{iframe_id}', name='{iframe_name}'")
except Exception as e:
    print(f"   Error checking frames: {e}")

# Try to find Next button
print("\n6. Looking for Next button...")
try:
    # Try sco frame first
    try:
        clicker.driver.switch_to.frame("sco")
        print("   ✅ Found 'sco' frame - this is a tab-based course")
        clicker.driver.switch_to.default_content()
    except:
        print("   ❌ No 'sco' frame - this is a popup window course")
    
    # Try to find Next button
    result = clicker.click_next()
    if result:
        print("   ✅ Successfully found and clicked Next button!")
    else:
        print("   ❌ Could not find Next button")
        
except Exception as e:
    print(f"   Error: {e}")

print("\n" + "="*60)
print("Debug complete! Check the output above.")
print("="*60)
print("\nLeaving browser open for inspection...")
print("Press Ctrl+C to exit")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nExiting...")

