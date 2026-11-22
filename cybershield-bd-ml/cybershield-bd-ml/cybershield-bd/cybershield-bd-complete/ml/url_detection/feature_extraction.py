
from __future__ import annotations

import ipaddress
import re
from urllib.parse import urlparse

# Deterministic, ordered feature schema. Both training and inference
# must produce a dict with exactly these keys, in this order.
FEATURE_SCHEMA = [
    "URLLength",
    "DomainLength",
    "IsDomainIP",
    "TLDLength",
    "NoOfSubDomain",
    "NoOfLettersInURL",
    "LetterRatioInURL",
    "NoOfDegitsInURL",
    "DegitRatioInURL",
    "NoOfEqualsInURL",
    "NoOfQMarkInURL",
    "NoOfAmpersandInURL",
    "NoOfOtherSpecialCharsInURL",
    "SpacialCharRatioInURL",
    "IsHTTPS",
    "NoOfObfuscatedChar",
    "ObfuscationRatio",
    "HasObfuscation",
]

_PERCENT_ENCODED_RE = re.compile(r"%[0-9A-Fa-f]{2}")


def _is_ip_address(host: str) -> bool:
    """Return True if host is a literal IPv4 or IPv6 address."""
    if not host:
        return False
    candidate = host.strip("[]")  # IPv6 literals in URLs are wrapped in [ ]
    try:
        ipaddress.ip_address(candidate)
        return True
    except ValueError:
        return False


def _safe_parse(url: str):
    """
    Parse a URL that may be missing a scheme (e.g. "example.com/login")
    without raising. Returns a urllib.parse.ParseResult.
    """
    url = url.strip()
    if "://" not in url:
        # No scheme given at all -> assume http for parsing purposes only.
        # This does NOT affect the IsHTTPS feature, which looks at the
        # ORIGINAL string, not this fallback.
        url_for_parsing = "http://" + url
    else:
        url_for_parsing = url
    try:
        return urlparse(url_for_parsing)
    except Exception:
        return urlparse("http://invalid-url-placeholder")


def extract_url_features(url: str) -> dict:
    
    if url is None:
        url = ""
    original = str(url).strip()

    if len(original) == 0:
        # Degenerate input: return a well-formed zero vector rather than crash.
        return {key: 0 for key in FEATURE_SCHEMA}

    parsed = _safe_parse(original)
    hostname = parsed.hostname or ""

    # ---- length-based ----
    url_length = len(original)
    domain_length = len(hostname)

    # ---- domain / TLD / subdomains ----
    is_domain_ip = 1 if _is_ip_address(hostname) else 0

    if is_domain_ip or not hostname:
        tld = ""
        no_of_subdomain = 0
    else:
        labels = [lbl for lbl in hostname.split(".") if lbl != ""]
        if len(labels) <= 1:
            tld = labels[0] if labels else ""
            no_of_subdomain = 0
        else:
            tld = labels[-1]
            # Everything before "domain.tld" counts as a subdomain level.
            no_of_subdomain = max(0, len(labels) - 2)

    tld_length = len(tld)

    # ---- character composition (computed on the ORIGINAL full URL) ----
    no_of_letters = sum(c.isalpha() for c in original)
    letter_ratio = no_of_letters / url_length if url_length else 0.0

    no_of_digits = sum(c.isdigit() for c in original)
    digit_ratio = no_of_digits / url_length if url_length else 0.0

    no_of_equals = original.count("=")
    no_of_qmark = original.count("?")
    no_of_ampersand = original.count("&")

    total_special_chars = sum(1 for c in original if not c.isalnum())
    # "Other" special chars = all non-alphanumeric chars minus the ones
    # already counted individually above (=, ?, &).
    no_of_other_special = max(
        0, total_special_chars - no_of_equals - no_of_qmark - no_of_ampersand
    )
    special_char_ratio = total_special_chars / url_length if url_length else 0.0

    # ---- scheme ----
    scheme = (parsed.scheme or "").lower()
    if "://" in original:
        is_https = 1 if original.lower().startswith("https://") else 0
    else:
        # No scheme was actually present in the input string at all.
        # We do not assume HTTPS in that case.
        is_https = 0

    # ---- obfuscation (percent-encoded characters, e.g. %20, %3A) ----
    obf_matches = _PERCENT_ENCODED_RE.findall(original)
    no_of_obfuscated_char = len(obf_matches)
    obfuscation_ratio = no_of_obfuscated_char / url_length if url_length else 0.0
    has_obfuscation = 1 if no_of_obfuscated_char > 0 else 0

    return {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "IsDomainIP": is_domain_ip,
        "TLDLength": tld_length,
        "NoOfSubDomain": no_of_subdomain,
        "NoOfLettersInURL": no_of_letters,
        "LetterRatioInURL": letter_ratio,
        "NoOfDegitsInURL": no_of_digits,
        "DegitRatioInURL": digit_ratio,
        "NoOfEqualsInURL": no_of_equals,
        "NoOfQMarkInURL": no_of_qmark,
        "NoOfAmpersandInURL": no_of_ampersand,
        "NoOfOtherSpecialCharsInURL": no_of_other_special,
        "SpacialCharRatioInURL": special_char_ratio,
        "IsHTTPS": is_https,
        "NoOfObfuscatedChar": no_of_obfuscated_char,
        "ObfuscationRatio": obfuscation_ratio,
        "HasObfuscation": has_obfuscation,
    }
