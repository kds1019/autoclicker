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

    # Read the Next control by ID (getElementById is reliable on CtSys even when
    # the element reports a zero box, which breaks Selenium's is_displayed()).
    _NEXT_JS = """
        var el = document.getElementById('next-btn');
        if (!el) return null;
        var cs = window.getComputedStyle(el);
        return {cls: (el.className || '').toString().toLowerCase(),
                display: cs.display,
                visibility: cs.visibility};
    """

    # Read the quiz/finish control by ID. "shown" ignores element size (the
    # control can be a zero-box flex container) and keys on display/visibility.
    _SUBMIT_JS = """
        var el = document.getElementById('submit-btn');
        if (!el) return null;
        var cs = window.getComputedStyle(el);
        var shown = cs.display !== 'none' && cs.visibility !== 'hidden'
                    && parseFloat(cs.opacity || '1') > 0.1
                    && el.offsetParent !== null;
        return {text: (el.textContent || '').trim(), shown: shown};
    """

    def _question_present(self):
        try:
            st = self.driver.execute_script(self._SUBMIT_JS)
        except Exception:
            return False
        if not st or not st.get("shown"):
            return False
        text = (st.get("text") or "").lower()
        if any(x.lower() in text for x in SUBMIT_EXCLUDE_KEYWORDS):
            return False
        return True

    def _next_ready(self):
        """True = highlighted/ready, False = present but not ready, None = not in DOM."""
        try:
            st = self.driver.execute_script(self._NEXT_JS)
        except Exception:
            return None
        if not st:
            return None
        cls = st.get("cls") or ""
        print(f"  ℹ️  Next state: cls='{cls}' display='{st.get('display')}'")
        if "submit-btn-off" in cls:
            return False
        if "submit-btn-on" in cls:
            return True
        return False  # unknown -> treat as not ready (safer for credit)

    def _click_next(self):
        try:
            ok = self.driver.execute_script(
                "var el=document.getElementById('next-btn');"
                "if(el){el.click();return true;}return false;"
            )
            return bool(ok)
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
