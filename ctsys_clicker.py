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

import os
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

    # ---- Deep (cross-frame) DOM helpers -------------------------------------
    # CtSys is an Angular app; the player controls (#next-btn / #submit-btn) and
    # the media may live in the top document OR inside a same-origin iframe.
    # These scripts collect the top document plus every ACCESSIBLE frame document
    # and search all of them, so it doesn't matter which frame Selenium focuses.

    _DOCS_FN = """
        function _docs(){
            var out=[];
            (function walk(d){
                out.push(d);
                var fr=d.querySelectorAll('iframe,frame');
                for(var i=0;i<fr.length;i++){
                    try{ var cd=fr[i].contentDocument; if(cd) walk(cd); }catch(e){}
                }
            })(document);
            return out;
        }
    """

    _NEXT_JS = _DOCS_FN + """
        var ds=_docs();
        for(var i=0;i<ds.length;i++){
            var el=ds[i].getElementById('next-btn');
            if(el){
                var cs=(el.ownerDocument.defaultView||window).getComputedStyle(el);
                return {cls:(el.className||'').toString().toLowerCase(),
                        display:cs.display, visibility:cs.visibility};
            }
        }
        return null;
    """

    _SUBMIT_JS = _DOCS_FN + """
        var ds=_docs();
        for(var i=0;i<ds.length;i++){
            var el=ds[i].getElementById('submit-btn');
            if(el){
                var cs=(el.ownerDocument.defaultView||window).getComputedStyle(el);
                var shown=cs.display!=='none' && cs.visibility!=='hidden'
                          && parseFloat(cs.opacity||'1')>0.1 && el.offsetParent!==null;
                return {text:(el.textContent||'').trim(), shown:shown};
            }
        }
        return null;
    """

    _MEDIA_JS = _DOCS_FN + """
        var ds=_docs(), playing=false;
        for(var i=0;i<ds.length;i++){
            ds[i].querySelectorAll('video,audio').forEach(function(m){
                try{ if(!m.paused && !m.ended && m.duration>0 &&
                        (m.duration-m.currentTime)>1) playing=true; }catch(e){}
            });
        }
        return playing;
    """

    _MUTE_JS = _DOCS_FN + """
        var ds=_docs();
        for(var i=0;i<ds.length;i++){
            ds[i].querySelectorAll('video').forEach(function(v){ v.muted=true; });
            ds[i].querySelectorAll('audio').forEach(function(a){ a.muted=true; });
        }
    """

    _CLICK_JS = _DOCS_FN + """
        var ds=_docs();
        for(var i=0;i<ds.length;i++){
            var el=ds[i].getElementById('next-btn');
            if(el){ el.click(); return true; }
        }
        return false;
    """

    # Diagnostic: describe every frame and where the controls live.
    _DIAG_JS = _DOCS_FN + """
        var out={topHasNext: !!document.getElementById('next-btn'),
                 topHasSubmit: !!document.getElementById('submit-btn'),
                 frames: []};
        var fr=document.querySelectorAll('iframe,frame');
        for(var i=0;i<fr.length;i++){
            var f={src:(fr[i].src||''), accessible:false, hasNext:false, hasSubmit:false};
            try{ var d=fr[i].contentDocument;
                 if(d){ f.accessible=true;
                        f.hasNext=!!d.getElementById('next-btn');
                        f.hasSubmit=!!d.getElementById('submit-btn'); } }catch(e){}
            out.frames.push(f);
        }
        return out;
    """

    def _to_main(self):
        try:
            self.driver.switch_to.default_content()
        except Exception:
            pass

    def _mute_quiet(self):
        """Mute media across all frames without printing (avoids log spam)."""
        try:
            self.driver.execute_script(self._MUTE_JS)
        except Exception:
            pass

    def _media_playing(self):
        try:
            return bool(self.driver.execute_script(self._MEDIA_JS))
        except Exception:
            return False

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

    def _diagnose(self):
        """Print where #next-btn / #submit-btn actually live (top vs frames) and
        also write it to ctsys_diagnostic.txt so it can be shared without needing
        to scroll/copy the console."""
        try:
            d = self.driver.execute_script(self._DIAG_JS)
        except Exception as e:
            print(f"  ⚠️  Diagnostic failed: {e}")
            return

        lines = [
            f"🩺 DIAG topHasNext={d.get('topHasNext')} "
            f"topHasSubmit={d.get('topHasSubmit')} frames={len(d.get('frames') or [])}"
        ]
        for i, f in enumerate(d.get("frames") or []):
            lines.append(
                f"    frame{i}: accessible={f.get('accessible')} "
                f"hasNext={f.get('hasNext')} hasSubmit={f.get('hasSubmit')} "
                f"src={f.get('src')}"
            )
        try:
            lines.insert(0, f"url={self.driver.current_url}")
        except Exception:
            pass

        for ln in lines:
            print("  " + ln)

        try:
            path = os.path.join(os.getcwd(), "ctsys_diagnostic.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write("\n".join(lines) + "\n")
            print(f"  📝 Saved diagnostic to: {path}")
        except Exception as e:
            print(f"  ⚠️  Could not write diagnostic file: {e}")

    def _click_next(self):
        try:
            return bool(self.driver.execute_script(self._CLICK_JS))
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
        not_found_streak = 0  # throttle the diagnostic so it prints once, not every loop
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
                    print("  🔎 Next button not found in any frame yet - waiting...")
                    if not_found_streak == 0:
                        self._diagnose()  # one-time layout dump so we can locate it
                    not_found_streak += 1
                    time.sleep(POLL_INTERVAL)
                    continue
                not_found_streak = 0
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
