import os
import sys
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", ".."))

from app import app
from ml.url_detection.feature_extraction import FEATURE_SCHEMA, extract_url_features
from ml.url_detection.xai import _load, explain_url


LEGITIMATE_URLS = [
    "https://www.google.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.wikipedia.org",
    "https://www.amazon.com",
]

PHISHING_URLS = [
    "http://192.168.0.1/login?verify=account",
    "http://secure-login-account.example.com/verify",
    "http://paypal-login-example.example.com/login",
]


def test_legitimate_urls_stay_safe_and_use_correct_probability_mapping():
    for url in LEGITIMATE_URLS:
        result = explain_url(url)
        assert result["prediction"] == 1, f"{url} should be legitimate according to the model"
        assert result["label"] == "legitimate"
        assert result["phishing_probability"] <= 50, f"{url} should not be flagged as phishing by class probability"
        assert result["legitimate_probability"] > result["phishing_probability"]
        assert result["status"] == "SAFE", f"{url} should remain SAFE if the model predicts legitimate"


def test_phishing_urls_are_flagged_using_phishing_class_probability():
    for url in PHISHING_URLS:
        result = explain_url(url)
        assert result["prediction"] == 0, f"{url} should be flagged as phishing by the model"
        assert result["label"] == "phishing"
        assert result["phishing_probability"] >= 80, f"{url} should have a strong phishing probability"
        assert result["status"] in {"SUSPICIOUS", "DANGEROUS"}, f"{url} should be suspicious or dangerous, not safe"


def test_trailing_slash_urls_match_model_features_and_probability_mapping():
    model, scaler = _load()
    client = app.test_client()
    urls = [
        "https://www.google.com/",
        "https://www.microsoft.com/",
        "https://www.apple.com/",
        "https://www.wikipedia.org/",
        "https://www.python.org/",
    ]

    for url in urls:
        features = extract_url_features(url)
        X = pd.DataFrame([[features[name] for name in FEATURE_SCHEMA]], columns=FEATURE_SCHEMA)
        model_input = scaler.transform(X) if scaler is not None else X
        predicted_class = int(model.predict(model_input)[0])
        raw_probabilities = model.predict_proba(model_input)[0]
        probabilities_by_class = {
            int(label): float(probability)
            for label, probability in zip(model.classes_, raw_probabilities)
        }
        result = explain_url(url)
        api_result = client.post("/api/analyze/url", json={"url": url}).get_json()

        assert result["prediction"] == predicted_class
        assert result["phishing_probability"] == probabilities_by_class[0] * 100
        assert result["legitimate_probability"] == probabilities_by_class[1] * 100
        assert result["risk_score"] == result["phishing_probability"]
        assert api_result["risk_score"] == result["risk_score"]
        assert api_result["phishing_probability"] == result["phishing_probability"]
        assert result["status"] == ("SAFE" if predicted_class == 1 else "DANGEROUS" if probabilities_by_class[0] >= 0.8 else "SUSPICIOUS")


def test_feature_contribution_explanations_match_contribution_sign():
    result = explain_url("http://secure-account-verify.example.com/login")
    for factor in result["top_factors"]:
        effect = "increases" if factor["contribution"] < 0 else "decreases" if factor["contribution"] > 0 else "does not change"
        assert effect in factor["explanation"]
