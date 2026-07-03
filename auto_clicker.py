"""
Training Auto-Clicker
Automatically clicks through training slides and alerts when questions appear
Supports multiple training systems (FlightSafety, CtSys) via config.py
Cross-platform: Works on Windows, Mac, and Linux
"""

import time
import random
import os
import platform
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from config import *

class TrainingAutoClicker:
    def __init__(self, gui_mode=False):
        self.driver = None
        self.running = False
        self.paused = False
        self.gui_mode = gui_mode  # Skip input() prompts in GUI mode
        
    def setup_browser(self):
        """Launch Chrome browser automatically and open the training site"""
        print("🔧 Launching Chrome browser...")

        options = webdriver.ChromeOptions()
        # Keep browser open after script ends
        options.add_experimental_option("detach", True)
        # Optional: start maximized
        options.add_argument("--start-maximized")

        try:
            # Automatically download and setup ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            print("✅ Chrome launched!")

            # Open the training website
            print(f"🌐 Opening {SITE_NAME} website: {TRAINING_URL}")
            self.driver.get(TRAINING_URL)

            if not self.gui_mode:
                print("\n📋 INSTRUCTIONS:")
                print(f"1. Login to {SITE_NAME} in the Chrome window")
                print("2. Click 'LAUNCH' or 'VIEW COURSE' to start your course")
                print("3. Wait for the course to open in a NEW TAB")
                print("4. Press ENTER here when the course tab is open...")
                input()

                # Switch to the newest tab (the course tab)
                print("\n🔄 Switching to course tab...")
                all_tabs = self.driver.window_handles
                if len(all_tabs) > 1:
                    self.driver.switch_to.window(all_tabs[-1])  # Switch to last/newest tab
                    print(f"✅ Switched to course tab (found {len(all_tabs)} tabs total)")
                    # Mute the course audio
                    self.mute_tab()
                else:
                    print("⚠️  Only 1 tab found - make sure you clicked LAUNCH!")

            return True
        except Exception as e:
            print(f"❌ Could not launch Chrome: {e}")
            print("\n⚠️  Make sure ChromeDriver is installed:")
            print("Run: pip install webdriver-manager")
            return False
    
    def play_alert(self):
        """Play beep sound to alert user - cross-platform"""
        print("\n🔊 QUESTION DETECTED! BEEPING...")
        system = platform.system()

        for _ in range(BEEP_COUNT):
            if system == "Darwin":  # macOS
                # Use afplay with system sound
                os.system('afplay /System/Library/Sounds/Ping.aiff')
            elif system == "Windows":
                # Use winsound (Windows only)
                import winsound
                winsound.Beep(BEEP_FREQUENCY, BEEP_DURATION)
            else:  # Linux
                # Use system beep command
                os.system('beep -f {} -l {}'.format(BEEP_FREQUENCY, BEEP_DURATION))
            time.sleep(0.2)
    
    def find_button(self, keywords, debug=False, exclude=None):
        """Find button by text content or attributes.

        exclude: optional list of substrings; any candidate whose text
        contains one of these is skipped (used to ignore non-quiz widgets
        like a "Submit Feedback" chat button).
        """
        all_buttons = []

        def _visible(el):
            # Skip elements hidden in the DOM - many training pages keep a
            # hidden Submit/Next in the markup that would cause false matches.
            try:
                return el.is_displayed()
            except:
                return False

        try:
            # Collect all clickable elements
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            for button in buttons:
                if not _visible(button):
                    continue
                button_text = button.text.strip()
                if button_text:
                    all_buttons.append(("button", button_text, button))

            inputs = self.driver.find_elements(By.TAG_NAME, "input")
            for input_elem in inputs:
                if input_elem.get_attribute("type") in ["button", "submit"]:
                    if not _visible(input_elem):
                        continue
                    input_value = input_elem.get_attribute("value") or ""
                    if input_value:
                        all_buttons.append(("input", input_value, input_elem))

            links = self.driver.find_elements(By.TAG_NAME, "a")
            for link in links:
                if not _visible(link):
                    continue
                link_text = link.text.strip()
                if link_text and len(link_text) < 50:  # Only show short link texts
                    all_buttons.append(("link", link_text, link))

            # Also check for div elements with onclick handlers (common in popup windows)
            divs = self.driver.find_elements(By.TAG_NAME, "div")
            for div in divs:
                onclick = div.get_attribute("onclick")
                if onclick:  # Has onclick handler
                    if not _visible(div):
                        continue
                    div_text = div.text.strip()
                    div_id = div.get_attribute("id") or ""
                    div_class = div.get_attribute("class") or ""
                    # Only include if it has text or a relevant id/class
                    if div_text and len(div_text) < 50:
                        all_buttons.append(("div", div_text, div))
                    elif "next" in div_id.lower() or "next" in div_class.lower():
                        display_text = div_text or f"(id:{div_id})" or f"(class:{div_class})"
                        all_buttons.append(("div", display_text, div))
        except Exception as e:
            if debug:
                print(f"  ⚠️ Error collecting buttons: {e}")

        # Debug output
        if debug:
            if all_buttons:
                print(f"  Found {len(all_buttons)} clickable elements:")
                for btn_type, btn_text, _ in all_buttons[:10]:
                    print(f"    [{btn_type}] '{btn_text}'")
            else:
                print("  ⚠️ No buttons/links found!")

        # Try to match keywords
        for keyword in keywords:
            for btn_type, btn_text, element in all_buttons:
                if keyword.lower() in btn_text.lower():
                    # Skip excluded (non-quiz) widgets like "Submit Feedback"
                    if exclude and any(x.lower() in btn_text.lower() for x in exclude):
                        if debug:
                            print(f"  ⏭️  Ignoring excluded match in <{btn_type}>: '{btn_text}'")
                        continue
                    if debug:
                        print(f"  ✅ Matched '{keyword}' in <{btn_type}>: '{btn_text}'")
                    return element

        return None
    
    def mute_tab(self):
        """Mute the current browser tab"""
        try:
            # Use JavaScript to mute all audio/video elements
            self.driver.execute_script("""
                // Mute all video elements
                document.querySelectorAll('video').forEach(v => v.muted = true);
                // Mute all audio elements
                document.querySelectorAll('audio').forEach(a => a.muted = true);
                // Also try to mute in the sco frame
                try {
                    var scoFrame = document.querySelector('frame[name="sco"]');
                    if (scoFrame && scoFrame.contentDocument) {
                        scoFrame.contentDocument.querySelectorAll('video').forEach(v => v.muted = true);
                        scoFrame.contentDocument.querySelectorAll('audio').forEach(a => a.muted = true);
                    }
                } catch(e) {}
            """)
            print("🔇 Course audio muted (beeps will still play)")
            return True
        except Exception as e:
            print(f"⚠️  Could not mute tab: {e}")
            return False

    def switch_to_course_tab_and_mute(self):
        """Switch to the newest window/tab (course window) and mute it - called by GUI"""
        try:
            print("\n🔄 Switching to course window/tab...")

            # Wait a moment for popup window to open
            time.sleep(3)  # Increased wait time for popup windows

            all_windows = self.driver.window_handles
            print(f"📊 Found {len(all_windows)} windows/tabs total")

            # Print all window titles for debugging
            for i, window_handle in enumerate(all_windows):
                self.driver.switch_to.window(window_handle)
                print(f"   Window {i+1}: '{self.driver.title}'")

            if len(all_windows) > 1:
                # Course opened in a new window/tab (e.g. FlightSafety popup)
                self.driver.switch_to.window(all_windows[-1])
                print(f"✅ Switched to newest window/tab: '{self.driver.title}'")
            else:
                # Course runs in the same window/tab (e.g. CtSys) - use it
                self.driver.switch_to.window(all_windows[0])
                print(f"ℹ️  Single window - using current tab: '{self.driver.title}'")

            # Wait a moment for content to load
            time.sleep(2)  # Increased wait time

            # Mute the course audio
            self.mute_tab()
            return True
        except Exception as e:
            print(f"❌ Error switching to course window: {e}")
            return False

    def switch_to_latest_course_tab(self):
        """Switch to the latest course window/tab (handles when user opens new course)"""
        try:
            # Wait a moment for new window to open
            time.sleep(2)

            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                # Switch to the last window/tab (newest - could be popup or tab)
                self.driver.switch_to.window(all_windows[-1])
                print(f"🔄 Switched to newest window (found {len(all_windows)} total)")
                # Mute the new window
                self.mute_tab()
                return True
            return False
        except Exception as e:
            return False

    def check_for_submit_button(self):
        """Check if Submit button exists (indicates question)"""
        try:
            # Make sure we're on the latest window (in case popup opened)
            all_windows = self.driver.window_handles
            if len(all_windows) > 1:
                # Always work with the last window (newest)
                self.driver.switch_to.window(all_windows[-1])

            submit_button = None

            # Try to find submit button in the content frame first
            try:
                self.driver.switch_to.frame(CONTENT_FRAME)
                submit_button = self.find_button(SUBMIT_BUTTON_KEYWORDS, debug=False, exclude=SUBMIT_EXCLUDE_KEYWORDS)
                self.driver.switch_to.default_content()
            except:
                # No "sco" frame - try main page (popup windows)
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass
                submit_button = self.find_button(SUBMIT_BUTTON_KEYWORDS, debug=False, exclude=SUBMIT_EXCLUDE_KEYWORDS)

            if submit_button:
                try:
                    matched = submit_button.text.strip() or submit_button.get_attribute("value") or "(no text)"
                except:
                    matched = "(unknown)"
                print(f"  🔍 Found submit button - question detected! (matched: '{matched}')")

            return submit_button is not None
        except Exception as e:
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            return False
    
    def is_next_ready(self, element):
        """Return True if the Next button is enabled/highlighted (slide complete).

        CtSys keeps Next dimmed/disabled until the slide finishes, then
        highlights it. We treat it as NOT ready if it shows any common
        "disabled" signal (aria-disabled, disabled attr/class, low opacity,
        pointer-events:none, not-allowed cursor). The state is logged so the
        exact signal can be tuned if needed.
        """
        try:
            info = self.driver.execute_script(
                """
                var el = arguments[0];
                var cs = window.getComputedStyle(el);
                return {
                    cls: (el.className || '').toString(),
                    ariaDisabled: el.getAttribute('aria-disabled'),
                    disabledAttr: el.getAttribute('disabled'),
                    opacity: cs.opacity,
                    pointerEvents: cs.pointerEvents,
                    cursor: cs.cursor
                };
                """,
                element,
            )
        except Exception as e:
            print(f"  ⚠️ Could not read Next button state: {e}")
            return True  # If we can't tell, don't block progress

        print(f"  ℹ️  Next button state: {info}")

        cls = (info.get("cls") or "").lower()
        # CtSys player marks the Next control explicitly: "submit-btn-on" when
        # the slide is complete (highlighted/clickable) and "submit-btn-off"
        # while it is still in progress. Key on that directly.
        if "submit-btn-off" in cls:
            return False
        if "submit-btn-on" in cls:
            return True
        if info.get("ariaDisabled") == "true":
            return False
        if info.get("disabledAttr") is not None:
            return False
        if "disable" in cls or "inactive" in cls or "not-active" in cls:
            return False
        try:
            if float(info.get("opacity") or "1") < 0.5:
                return False
        except Exception:
            pass
        if (info.get("pointerEvents") or "") == "none":
            return False
        if (info.get("cursor") or "") == "not-allowed":
            return False
        return True

    def click_next(self):
        """Find and click the Next button"""
        next_button = None

        try:
            print("🖱️  Looking for Next button...")

            # Make sure we're on the latest window (in case popup opened)
            all_windows = self.driver.window_handles
            print(f"  📊 Total windows/tabs: {len(all_windows)}")

            if len(all_windows) > 1:
                # Always work with the last window (newest)
                self.driver.switch_to.window(all_windows[-1])
                window_title = self.driver.title
                print(f"  🪟 Switched to window: '{window_title}' (total: {len(all_windows)} windows)")
            else:
                window_title = self.driver.title
                print(f"  🪟 Current window: '{window_title}'")

            # Re-mute audio before checking (in case volume button was pressed)
            self.mute_tab()

            # Try to find button in the content frame first (most courses)
            try:
                self.driver.switch_to.frame(CONTENT_FRAME)
                next_button = self.find_button(NEXT_BUTTON_KEYWORDS, debug=True)

                if next_button:
                    # Check if button is enabled (not disabled)
                    is_disabled = next_button.get_attribute("aria-disabled") == "true"
                    if is_disabled:
                        print("⚠️  Next button is disabled (video/audio still playing)")
                        self.driver.switch_to.default_content()
                        return False

                    try:
                        # Use JavaScript click to avoid element interception issues
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print("✅ Clicked Next (in sco frame)")
                        self.driver.switch_to.default_content()
                        # Mute again after clicking (new slide might have audio)
                        time.sleep(0.5)
                        self.mute_tab()
                        return True
                    except Exception as e:
                        print(f"⚠️  Could not click Next: {e}")
                        self.driver.switch_to.default_content()
                        return False
                else:
                    self.driver.switch_to.default_content()

            except Exception as frame_error:
                # No content frame - try looking directly on the page (popup windows)
                print(f"⚠️  No '{CONTENT_FRAME}' frame found - this appears to be a popup window course")
                print(f"   Current URL: {self.driver.current_url}")
                try:
                    self.driver.switch_to.default_content()
                except:
                    pass

                # Debug: Check if there are any frames at all
                try:
                    frames = self.driver.find_elements(By.TAG_NAME, "frame")
                    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
                    print(f"🔍 Found {len(frames)} <frame> elements and {len(iframes)} <iframe> elements")

                    # Show iframe details
                    if iframes:
                        print(f"  📋 iframes found:")
                        for i, iframe in enumerate(iframes):
                            iframe_id = iframe.get_attribute("id")
                            iframe_name = iframe.get_attribute("name")
                            iframe_src = iframe.get_attribute("src")
                            iframe_class = iframe.get_attribute("class")
                            is_visible = iframe.is_displayed()
                            visibility = "✅" if is_visible else "❌"
                            print(f"     {i+1}. {visibility} id='{iframe_id}', name='{iframe_name}', class='{iframe_class}'")
                            if iframe_src:
                                print(f"         src: {iframe_src[:100]}")

                    # Try each frame to find the Next button
                    for i, frame in enumerate(frames + iframes):
                        try:
                            frame_name = frame.get_attribute("name") or frame.get_attribute("id") or f"frame_{i}"
                            print(f"  📄 Trying frame: {frame_name}")
                            self.driver.switch_to.frame(frame)
                            next_button = self.find_button(NEXT_BUTTON_KEYWORDS, debug=True)
                            if next_button:
                                print(f"✅ Found Next button in frame: {frame_name}")
                                # Check if button is enabled
                                is_disabled = next_button.get_attribute("aria-disabled") == "true"
                                if is_disabled:
                                    print("⚠️  Next button is disabled (video/audio still playing)")
                                    self.driver.switch_to.default_content()
                                    return False

                                # Click it!
                                self.driver.execute_script("arguments[0].click();", next_button)
                                print(f"✅ Clicked Next (in frame: {frame_name})")
                                self.driver.switch_to.default_content()
                                time.sleep(0.5)
                                self.mute_tab()
                                return True
                            self.driver.switch_to.default_content()
                        except Exception as e:
                            try:
                                self.driver.switch_to.default_content()
                            except:
                                pass
                except Exception as e:
                    print(f"⚠️  Error checking frames: {e}")

                # Look for Next button directly on the page
                print("🔍 Looking for Next button on main page...")

                # Check if video is playing
                try:
                    videos = self.driver.find_elements(By.TAG_NAME, "video")
                    if videos:
                        for video in videos:
                            is_paused = self.driver.execute_script("return arguments[0].paused;", video)
                            current_time = self.driver.execute_script("return arguments[0].currentTime;", video)
                            duration = self.driver.execute_script("return arguments[0].duration;", video)

                            if not is_paused and duration > 0:
                                remaining = duration - current_time
                                print(f"  🎬 Video playing: {int(current_time)}s / {int(duration)}s (⏳ {int(remaining)}s remaining)")
                                print(f"  ⏸️  Waiting for video to finish...")
                                return False  # Don't click yet, video still playing
                except Exception as e:
                    pass  # No video or error checking

                # Check if video is playing
                try:
                    videos = self.driver.find_elements(By.TAG_NAME, "video")
                    if videos:
                        for video in videos:
                            try:
                                is_paused = self.driver.execute_script("return arguments[0].paused;", video)
                                current_time = self.driver.execute_script("return arguments[0].currentTime;", video)
                                duration = self.driver.execute_script("return arguments[0].duration;", video)

                                if duration and duration > 0:
                                    remaining = duration - current_time
                                    if not is_paused and remaining > 1:
                                        print(f"  🎬 Video playing: {int(current_time)}s / {int(duration)}s (⏳ {int(remaining)}s remaining)")
                                        print(f"  ⏸️  Waiting for video to finish before Next button appears...")
                                        return False  # Don't click yet, video still playing
                                    elif remaining <= 1:
                                        print(f"  ✅ Video finished! Next button should appear soon...")
                            except:
                                pass
                except Exception as e:
                    pass  # No video or error checking

                # Debug: Show all buttons and links on page
                try:
                    all_buttons = self.driver.find_elements(By.TAG_NAME, "button")
                    all_links = self.driver.find_elements(By.TAG_NAME, "a")
                    print(f"  🔢 Found {len(all_buttons)} buttons, {len(all_links)} links")

                    # Show visible buttons only
                    visible_buttons = [b for b in all_buttons if b.is_displayed()]
                    if visible_buttons:
                        print(f"  📋 Visible buttons ({len(visible_buttons)}):")
                        for i, btn in enumerate(visible_buttons[:20]):
                            btn_text = btn.text.strip()
                            btn_aria = btn.get_attribute("aria-label")
                            btn_title = btn.get_attribute("title")
                            btn_class = btn.get_attribute("class")
                            display_text = btn_text or btn_aria or btn_title or f"(class:{btn_class})"
                            print(f"     {i+1}. {display_text}")

                    # Show visible links with more details
                    visible_links = [l for l in all_links if l.is_displayed()]
                    if visible_links:
                        print(f"  🔗 Visible links ({len(visible_links)}):")
                        for i, link in enumerate(visible_links[:20]):
                            link_text = link.text.strip()
                            link_aria = link.get_attribute("aria-label")
                            link_title = link.get_attribute("title")
                            link_class = link.get_attribute("class")
                            link_href = link.get_attribute("href")
                            link_id = link.get_attribute("id")

                            # Get innerHTML to see what's inside
                            try:
                                inner_html = self.driver.execute_script("return arguments[0].innerHTML;", link)
                            except:
                                inner_html = ""

                            display_text = link_text or link_aria or link_title or f"(id:{link_id})" or f"(class:{link_class})"
                            print(f"     {i+1}. {display_text}")
                            if not link_text and inner_html:
                                print(f"         innerHTML: {inner_html[:150]}")
                            if link_href and link_href != "javascript:void(0);" and not link_href.startswith("http"):
                                print(f"         href: {link_href[:100]}")
                except Exception as e:
                    print(f"  ⚠️ Error listing elements: {e}")

                # First check for "Start Course" button (intro page)
                start_button = self.find_button(["Start Course", "BEGIN", "START"], debug=False)
                if start_button:
                    try:
                        print("🎬 Found 'Start Course' button - clicking to begin...")
                        self.driver.execute_script("arguments[0].click();", start_button)
                        time.sleep(2)  # Wait for course to load
                        self.mute_tab()
                        return False  # Don't count as Next click, just starting
                    except Exception as e:
                        print(f"⚠️  Could not click Start Course: {e}")

                # Check for "I Accept" button (terms page)
                accept_button = self.find_button(["I Accept", "ACCEPT", "AGREE"], debug=False)
                if accept_button:
                    try:
                        print("✅ Found 'I Accept' button - accepting terms...")
                        self.driver.execute_script("arguments[0].click();", accept_button)
                        time.sleep(2)  # Wait for next page
                        self.mute_tab()
                        return False  # Don't count as Next click
                    except Exception as e:
                        print(f"⚠️  Could not click I Accept: {e}")

                # Try using JavaScript to find all clickable elements
                print("  🔍 Using JavaScript to find all clickable elements...")
                try:
                    # Get all elements with onclick or that are clickable
                    js_script = """
                    var elements = [];
                    var all = document.querySelectorAll('*');
                    for (var i = 0; i < all.length; i++) {
                        var el = all[i];
                        if (el.onclick || el.style.cursor === 'pointer' ||
                            el.getAttribute('role') === 'button' ||
                            (el.textContent && el.textContent.toLowerCase().includes('next'))) {
                            var visible = el.offsetWidth > 0 && el.offsetHeight > 0;
                            if (visible) {
                                elements.push({
                                    tag: el.tagName,
                                    text: el.textContent.trim().substring(0, 100),
                                    id: el.id,
                                    class: el.className,
                                    onclick: el.onclick ? 'yes' : 'no'
                                });
                            }
                        }
                    }
                    return elements;
                    """
                    clickable_elements = self.driver.execute_script(js_script)
                    if clickable_elements:
                        print(f"  ✅ Found {len(clickable_elements)} clickable elements via JavaScript:")
                        for i, el in enumerate(clickable_elements[:20]):
                            print(f"     {i+1}. <{el['tag']}> '{el['text'][:50]}' (id:{el['id']}, onclick:{el['onclick']})")
                except Exception as e:
                    print(f"  ⚠️ Error finding clickable elements: {e}")

                # Now look for Next button (try div with id="btnNext" first for popup windows)
                print("  🔍 Searching for Next button...")
                next_button = None

                # Try finding div with id="btnNext" (popup window courses)
                try:
                    next_button = self.driver.find_element(By.ID, "btnNext")
                    if next_button:
                        is_displayed = next_button.is_displayed()
                        print(f"  🔍 Found div#btnNext, is_displayed={is_displayed}")
                        if not is_displayed:
                            # Element exists but not visible, skip it
                            next_button = None
                        else:
                            print("  ✅ Found Next button (div#btnNext)")
                except Exception as e:
                    print(f"  ⚠️ div#btnNext not found: {e}")
                    pass

                # Also try other common popup window button IDs
                # ("next-btn" is the CtSys player's Next control)
                if not next_button:
                    for btn_id in ["next-btn", "nextBtn", "nextButton", "btnContinue", "next-button", "continueButton"]:
                        try:
                            next_button = self.driver.find_element(By.ID, btn_id)
                            if next_button and next_button.is_displayed():
                                print(f"  ✅ Found Next button (#{btn_id})")
                                break
                            else:
                                next_button = None
                        except:
                            pass

                # If not found, try the regular button search
                if not next_button:
                    next_button = self.find_button(NEXT_BUTTON_KEYWORDS, debug=True)

                if next_button:
                    # Only click once the slide is complete (button enabled/highlighted)
                    if not self.is_next_ready(next_button):
                        print("⚠️  Next button not ready yet (slide still in progress) - waiting")
                        return False

                    try:
                        # Use JavaScript click to avoid element interception issues
                        self.driver.execute_script("arguments[0].click();", next_button)
                        print("✅ Clicked Next (on main page)")
                        # Mute again after clicking (new slide might have audio)
                        time.sleep(0.5)
                        self.mute_tab()
                        return True
                    except Exception as e:
                        print(f"⚠️  Could not click Next: {e}")
                        return False

            print("⚠️  Next button not found")
            return False

        except Exception as e:
            print(f"⚠️  Error in click_next: {e}")
            try:
                self.driver.switch_to.default_content()
            except:
                pass
            # Try switching to latest window in case user opened new course
            if self.switch_to_latest_course_tab():
                print("🔄 Switched to newest course window")
            return False

    def wait_for_submit_to_disappear(self):
        """Wait for Submit button to disappear (user answered question)"""
        print("⏳ Waiting for you to answer the question and click Submit...")
        while self.check_for_submit_button():
            time.sleep(1)
        print("✅ Question answered! Resuming auto-clicking...")

    def run(self, skip_setup=False):
        """Main loop - auto-click through slides"""
        if not skip_setup:
            if not self.setup_browser():
                return

        print("\n" + "="*60)
        print(f"🚀 {SITE_NAME} Auto-Clicker Started!")
        print("="*60)
        print(f"⏱️  Random delay: {MIN_CLICK_DELAY}-{MAX_CLICK_DELAY} seconds between clicks")
        print(f"🔊 Will beep when questions detected")
        print(f"🛑 Press CTRL+C to stop")
        print("="*60 + "\n")

        self.running = True

        try:
            while self.running:
                if self.paused:
                    time.sleep(0.5)
                    continue

                # Check for Submit button (question detected)
                if self.check_for_submit_button():
                    print("\n" + "!"*60)
                    print("❓ QUESTION DETECTED!")
                    print("!"*60)
                    self.play_alert()
                    self.wait_for_submit_to_disappear()
                    continue

                # Click Next button
                print(f"\n🖱️  Looking for Next button...")
                if self.click_next():
                    # Random delay before next click
                    delay = random.randint(MIN_CLICK_DELAY, MAX_CLICK_DELAY)
                    print(f"⏳ Waiting {delay} seconds before next click...")
                    time.sleep(delay)
                else:
                    # If Next button not found, wait a bit and try again
                    print("⏳ Waiting 5 seconds and trying again...")
                    time.sleep(5)

        except KeyboardInterrupt:
            print("\n\n🛑 Stopped by user (CTRL+C)")
        finally:
            print("\n✅ Auto-clicker stopped")
            print("⚠️  Browser will stay open - close it manually when done")
            # Don't close browser - user is still using it


if __name__ == "__main__":
    clicker = TrainingAutoClicker()
    clicker.run()


