"""
CtSys Auto-Clicker (clean, CtSys-only path)

CtSys runs the course in a single tab (no popup, no SCORM "sco" frame),
exposes Next as <div id="next-btn"> (ready ONLY when its class includes
"submit-btn-on"), and shows the quiz/finish control as <div id="submit-btn">.

This module reuses the browser/beep helpers from TrainingAutoClicker but
replaces the tangled multi-path loop with one deterministic loop:
  1. If a question/finish control needs input -> beep and wait.
  2. If video OR audio is still playing -> wait (so the slide gets credit).
  3. Only click Next once it is highlighted (submit-btn-on).
  4. After it highlights, wait a RANDOM human-like time, then click.
"""

import time
import random

from selenium.webdriver.common.by import By

from auto_clicker import TrainingAutoClicker
from config import (
    SITE_NAME,
    SUBMIT_EXCLUDE_KEYWORDS,
    READY_TO_CLICK_MIN,
    READY_TO_CLICK_MAX,
    POLL_INTERVAL,
)


class CtSysClicker(TrainingAutoClicker):
    """Deterministic single-path clicker for training.ctsys.com."""

    _MEDIA_JS = """
        var playing = false;
        document.querySelectorAll('video,audio').forEach(function(m){
            try {
                if (!m.paused && !m.ended && m.duration > 0 &&
                    (m.duration - m.currentTime) > 1) playing = true;
            } catch (e) {}
        });
        return playing;
    """

    _MUTE_JS = """
        document.querySelectorAll('video').forEach(function(v){ v.muted = true; });
        document.querySelectorAll('audio').forEach(function(a){ a.muted = true; });
    """

    def _to_main(self):
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

    def _mute_quiet(self):
        """Mute media without printing (avoids per-loop log spam)."""
        try:
            self.driver.execute_script(self._MUTE_JS)
        except Exception:
            pass

    def _media_playing(self):
        try:
            return bool(self.driver.execute_script(self._MEDIA_JS))
        except Exception:
            return False

    def _find(self, element_id):
        """Return a visible element by id, or None. Uses Selenium's
        is_displayed() (robust) rather than a raw offsetWidth check."""
        try:
            el = self.driver.find_element(By.ID, element_id)
        except Exception:
            return None
        try:
            if not el.is_displayed():
                return None
        except Exception:
            pass
        return el

    def _question_present(self):
        el = self._find("submit-btn")
        if el is None:
            return False
        try:
            text = (el.text or "").lower()
        except Exception:
            text = ""
        if any(x.lower() in text for x in SUBMIT_EXCLUDE_KEYWORDS):
            return False
        return True

    def _next_ready(self):
        """True = highlighted/ready, False = present but not ready, None = not shown."""
        el = self._find("next-btn")
        if el is None:
            return None
        cls = (el.get_attribute("class") or "").lower()
        print(f"  ℹ️  Next state: cls='{cls}'")
        if "submit-btn-off" in cls:
            return False
        if "submit-btn-on" in cls:
            return True
        return False  # unknown -> treat as not ready (safer for credit)

    def _click_next(self):
        el = self._find("next-btn")
        if el is None:
            return False
        try:
            self.driver.execute_script("arguments[0].click();", el)
            return True
        except Exception as e:
            print(f"⚠️  Could not click Next: {e}")
            return False

    def run(self, skip_setup=False):
        if not skip_setup and not self.setup_browser():
            return

        print("\n" + "=" * 60)
        print(f"🚀 {SITE_NAME} Auto-Clicker Started (CtSys mode)!")
        print("=" * 60)
        print(f"⏱️  Waits {READY_TO_CLICK_MIN}-{READY_TO_CLICK_MAX}s (random) after "
              f"Next highlights, then clicks")
        print("🔊 Beeps when a question/submit needs your input")
        print("🛑 Press CTRL+C (or STOP) to stop")
        print("=" * 60 + "\n")

        self.running = True
        self.mute_tab()  # loud mute once so the user sees confirmation
        try:
            while self.running:
                if self.paused:
                    time.sleep(0.5)
                    continue

                self._to_main()
                self._mute_quiet()

                # 1) Question / finish control needs input -> beep and wait
                if self._question_present():
                    print("\n" + "!" * 60)
                    print("❓ QUESTION DETECTED! Waiting for you to answer/submit...")
                    print("!" * 60)
                    self.play_alert()
                    while self.running and self._question_present():
                        time.sleep(1)
                    print("✅ Input handled - resuming...")
                    continue

                # 2) Media still playing -> let the slide finish (for credit)
                if self._media_playing():
                    print("  🎬 Slide still playing - waiting...")
                    time.sleep(POLL_INTERVAL)
                    continue

                # 3) Is Next highlighted (slide complete)?
                ready = self._next_ready()
                if ready is None:
                    print("  🔎 Next button not on screen yet - waiting...")
                    time.sleep(POLL_INTERVAL)
                    continue
                if not ready:
                    print("  ⏳ Next not highlighted yet (slide in progress) - waiting...")
                    time.sleep(POLL_INTERVAL)
                    continue

                # 4) Highlighted: wait a random human-like time, then click
                delay = random.randint(READY_TO_CLICK_MIN, READY_TO_CLICK_MAX)
                print(f"  ✅ Slide complete - waiting {delay}s before clicking Next...")
                waited = 0
                while waited < delay and self.running:
                    time.sleep(1)
                    waited += 1
                    if self._question_present() or self._media_playing():
                        break
                if not self.running:
                    break
                # Re-verify nothing changed during the wait
                if (self._question_present() or self._media_playing()
                        or self._next_ready() is not True):
                    continue
                if self._click_next():
                    print("  ➡️  Clicked Next")
                    time.sleep(0.5)
                    self._mute_quiet()
        except KeyboardInterrupt:
            print("\n\n🛑 Stopped by user (CTRL+C)")
        finally:
            print("\n✅ Auto-clicker stopped (browser stays open)")
