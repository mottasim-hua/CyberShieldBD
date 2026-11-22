"""
text_preprocessing.py

Lightweight, reusable text cleaning for the spam/suspicious-message
detection module. Deliberately conservative: we do NOT strip URLs,
digits, or currency symbols, since those are meaningful signals for
spam/scam detection (e.g. "claim $1000", phone numbers, links).

This module is shared by:
  1. ml/message_detection/prepare_data.py  (training-time cleaning)
  2. the future Flask backend              (inference-time cleaning)
"""

import re

_WHITESPACE_RE = re.compile(r"\s+")
# Keep letters, digits, common currency symbols, and basic punctuation
# that can carry meaning (!, ?, $, £, %, @). Strip other noise/control
# characters only.
_NOISE_RE = re.compile(r"[^a-zA-Z0-9\s\.\,\!\?\$\%\@\:\/\-]")


def clean_text(text: str) -> str:
    """
    Normalize a raw message for TF-IDF vectorization.
    Never raises on None/empty/garbage input.
    """
    if text is None:
        return ""
    text = str(text)
    text = text.lower()
    text = _NOISE_RE.sub(" ", text)
    text = _WHITESPACE_RE.sub(" ", text).strip()
    return text
