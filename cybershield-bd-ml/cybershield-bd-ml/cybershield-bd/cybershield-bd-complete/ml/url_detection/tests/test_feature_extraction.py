"""
Basic unit tests for extract_url_features().

Run with:
    python -m ml.url_detection.tests.test_feature_extraction
from the project root, or via pytest if available.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from ml.url_detection.feature_extraction import extract_url_features, FEATURE_SCHEMA


def _assert_schema(features: dict):
    assert list(features.keys()) == FEATURE_SCHEMA, "Feature keys/order changed!"


def test_normal_https_url():
    f = extract_url_features("https://www.example.com/login")
    _assert_schema(f)
    assert f["IsHTTPS"] == 1
    assert f["IsDomainIP"] == 0
    assert f["URLLength"] == len("https://www.example.com/login")


def test_plain_http_url():
    f = extract_url_features("http://example.com/")
    _assert_schema(f)
    assert f["IsHTTPS"] == 0


def test_ip_based_url():
    f = extract_url_features("http://125.98.3.123/fake.html")
    _assert_schema(f)
    assert f["IsDomainIP"] == 1
    assert f["NoOfSubDomain"] == 0


def test_ipv6_url():
    f = extract_url_features("http://[2001:db8::1]/path")
    _assert_schema(f)
    assert f["IsDomainIP"] == 1


def test_suspicious_url_with_obfuscation_and_symbols():
    url = "http://secure-login.paypal.com.verify-user%20account.tk/path?cmd=login&id=1"
    f = extract_url_features(url)
    _assert_schema(f)
    assert f["NoOfObfuscatedChar"] >= 1
    assert f["HasObfuscation"] == 1
    assert f["NoOfAmpersandInURL"] == 1
    assert f["NoOfEqualsInURL"] == 2
    assert f["NoOfQMarkInURL"] == 1
    assert f["NoOfSubDomain"] >= 1


def test_url_missing_scheme():
    # Real users often paste bare domains without http(s)://
    f = extract_url_features("www.example.com/reset-password")
    _assert_schema(f)
    # No scheme literally present -> we must not assume HTTPS
    assert f["IsHTTPS"] == 0
    assert f["DomainLength"] > 0


def test_malformed_url_does_not_crash():
    for bad in ["", "   ", "http://", "not a url at all !!! ***", None]:
        f = extract_url_features(bad)
        _assert_schema(f)
        # must always return numeric values, never raise
        for v in f.values():
            assert isinstance(v, (int, float))


def test_empty_string_returns_zero_vector():
    f = extract_url_features("")
    _assert_schema(f)
    assert all(v == 0 for v in f.values())


def run_all():
    tests = [obj for name, obj in globals().items() if name.startswith("test_")]
    passed = 0
    for t in tests:
        t()
        passed += 1
        print(f"PASS: {t.__name__}")
    print(f"\n{passed}/{len(tests)} tests passed.")


if __name__ == "__main__":
    run_all()
