"""
Shared configuration for the ML gating prototype.
Defaults align with docs/plan.md.
"""
import os

WINDOW_SECONDS = 6
STRIDE_SECONDS = 1
GRACE_SECONDS = 25
DEV_MODE = os.getenv("DEV_MODE", "false").lower() == "true"

CONF_THRESH_UNLOCK = 0.72
CONF_THRESH_PROMPT = 0.45

ACTIONS = {
    "UNLOCK": "unlock",
    "DENY": "deny",
    "PROMPT": "prompt",
    "HOLD": "hold",
    "GRACE": "grace",
}

BANNER_COPY = {
    "offer_help": "Looks like you are thinking—want a hand from the assistant?",
    "request_effort": "Take a moment to outline or draft a bit more, then we will unlock help.",
    "hold": "Staying out of your way while you are in flow.",
}

LOG_PREFIX = "[DEV_MODE] "
