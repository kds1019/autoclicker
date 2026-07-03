"""
Configuration settings for the Training Auto-Clicker

Supports multiple online training systems (FlightSafety, CtSys).
Set TRAINING_SITE below to choose which one the browser opens.
"""

# ============================================================================
# WEBSITE SETTINGS
# ============================================================================

# Which training system to use: "flightsafety" or "ctsys"
TRAINING_SITE = "ctsys"

# Per-site settings. Each site defines:
#   name          - label shown in logs and the GUI
#   url           - page the browser opens automatically
#   content_frame - name of the SCORM/content frame to try first (the
#                   auto-clicker also scans every other frame as a fallback,
#                   so popup-window courses still work if this doesn't match)
TRAINING_SITES = {
    "flightsafety": {
        "name": "FlightSafety",
        "url": "https://fsi-customer.okta.com/oauth2/aus1kfqntg1hrJWLh4h7/v1/authorize?client_id=0oa2teif5oVCU9x5U4h7&response_type=code&scope=openid+https%3A%2F%2Fmfs2.flightsafety.com&state=https%3A%2F%2FMFS2.flightsafety.com&redirect_uri=https%3A%2F%2Fwww.flightsafety.com%2Fmfs_authorization_code_callback.php",
        "content_frame": "sco",
    },
    "ctsys": {
        "name": "CtSys",
        "url": "https://training.ctsys.com/login",
        "content_frame": "sco",
    },
}

# Active site (derived from TRAINING_SITE above)
_active_site = TRAINING_SITES[TRAINING_SITE]
SITE_NAME = _active_site["name"]
TRAINING_URL = _active_site["url"]
CONTENT_FRAME = _active_site["content_frame"]

# Backward-compatible alias (older code/imports referenced this name)
FLIGHTSAFETY_URL = TRAINING_SITES["flightsafety"]["url"]

# ============================================================================
# CLICK DELAY SETTINGS
# ============================================================================

# Random delay between clicks (in seconds)
MIN_CLICK_DELAY = 1   # Minimum delay (seconds)
MAX_CLICK_DELAY = 20  # Maximum delay (seconds)

# CtSys mode only: after the Next button highlights (slide complete), wait a
# RANDOM human-like time in this range before actually clicking it. This makes
# the timing look natural and lets the completed slide register for credit.
READY_TO_CLICK_MIN = 3   # Minimum wait after highlight (seconds)
READY_TO_CLICK_MAX = 12  # Maximum wait after highlight (seconds)

# CtSys mode only: how often to re-check the slide state while waiting (seconds)
POLL_INTERVAL = 3

# ============================================================================
# BUTTON DETECTION KEYWORDS
# ============================================================================

# Keywords to detect "Next" buttons (case-insensitive)
NEXT_BUTTON_KEYWORDS = [
    "next>",      # FlightSafety specific
    "next",
    "continue",
    "proceed",
    "forward",
    "next slide",
    "→",
    ">",
]

# Keywords to detect "Submit" buttons (indicates a question)
SUBMIT_BUTTON_KEYWORDS = [
    "submit",
    "submit answer",
    "submit response",
    "check answer",
]

# Text that looks like a Submit button but is NOT a quiz question
# (e.g. CtSys has a persistent "Submit Feedback" chat widget on every page).
# Any candidate whose text contains one of these is ignored by question detection.
SUBMIT_EXCLUDE_KEYWORDS = [
    "feedback",
    "chat",
]

# Additional question detection keywords (in page text)
QUESTION_KEYWORDS = [
    "question",
    "quiz",
    "select",
    "choose",
    "answer",
    "true or false",
    "multiple choice",
]

# ============================================================================
# NOTIFICATION SETTINGS
# ============================================================================

# Number of beeps when question detected
BEEP_COUNT = 5

# Beep frequency (Hz) - higher = higher pitch
BEEP_FREQUENCY = 1000

# Beep duration (milliseconds)
BEEP_DURATION = 500

# ============================================================================
# BROWSER SETTINGS
# ============================================================================

# Wait time for page elements to load (seconds)
PAGE_LOAD_WAIT = 3

# Maximum time to wait for an element (seconds)
ELEMENT_WAIT_TIMEOUT = 10

# ============================================================================
# SAFETY SETTINGS
# ============================================================================

# Emergency stop key (press this to stop the script immediately)
EMERGENCY_STOP_KEY = "esc"

# Pause key (press this to pause/resume)
PAUSE_KEY = "space"

