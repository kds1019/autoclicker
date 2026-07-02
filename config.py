"""
Configuration settings for FlightSafety Auto-Clicker
"""

# ============================================================================
# WEBSITE SETTINGS
# ============================================================================

# FlightSafety training website URL (Okta login)
FLIGHTSAFETY_URL = "https://fsi-customer.okta.com/oauth2/aus1kfqntg1hrJWLh4h7/v1/authorize?client_id=0oa2teif5oVCU9x5U4h7&response_type=code&scope=openid+https%3A%2F%2Fmfs2.flightsafety.com&state=https%3A%2F%2FMFS2.flightsafety.com&redirect_uri=https%3A%2F%2Fwww.flightsafety.com%2Fmfs_authorization_code_callback.php"

# ============================================================================
# CLICK DELAY SETTINGS
# ============================================================================

# Random delay between clicks (in seconds)
MIN_CLICK_DELAY = 1   # Minimum delay (seconds)
MAX_CLICK_DELAY = 20  # Maximum delay (seconds)

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

