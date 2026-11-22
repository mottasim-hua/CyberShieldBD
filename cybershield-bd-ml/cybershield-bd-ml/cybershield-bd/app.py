"""Flask API and local web interface for CyberShield BD."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

from flask import Flask, jsonify, render_template, request

from ml.message_detection.xai import explain_message
from ml.url_detection.xai import explain_url

BASE_DIR = Path(__file__).resolve().parent
URL_METRICS_PATH = BASE_DIR / "ml" / "results" / "url_model_metrics.json"
MESSAGE_METRICS_PATH = BASE_DIR / "ml" / "results" / "message_model_metrics.json"
MESSAGE_METADATA_PATH = BASE_DIR / "ml" / "message_detection" / "artifacts" / "message_model_metadata.json"

app = Flask(__name__, template_folder="templates", static_folder="static")


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as file:
        return json.load(file)


def valid_url(value: str) -> bool:
    """Validate pasted URLs without visiting the URL or using a third party."""
    if not value or any(character.isspace() for character in value):
        return False
    candidate = value if "://" in value else f"http://{value}"
    try:
        return bool(urlparse(candidate).hostname)
    except (TypeError, ValueError):
        return False


def url_response(url: str) -> dict:
    result = explain_url(url)
    risk_score = float(result["phishing_probability"])
    legitimate_probability = float(result["legitimate_probability"])
    risky = result["prediction"] == 0
    status = result["status"]
    warning = {
        "SAFE": "This link appears legitimate based on its URL patterns. No strong phishing indicators were detected.",
        "LOW_RISK": "The URL has a low phishing score, but check the destination before entering sensitive information.",
        "SUSPICIOUS": "This link shows several characteristics associated with phishing. Be careful before entering passwords, OTPs, or financial information.",
        "HIGH_RISK": "This link has a high phishing score. Avoid entering passwords, OTPs, or financial information.",
        "DANGEROUS": "This link appears strongly associated with phishing patterns. Avoid opening it or entering sensitive information.",
    }[status]
    recommendation = "Only enter sensitive information when you trust the website." if not risky else "Do not open the link or enter your password, PIN, or OTP."
    return {
        "type": "url", "input": url, "prediction": result["label"],
        "label": "Phishing" if risky else "Legitimate",
        "risk_score": risk_score,
        "phishing_probability": risk_score,
        "legitimate_probability": legitimate_probability,
        "status": status,
        "status_basis": "Risk is the model-estimated phishing probability, not a certainty; prediction is the model's class.",
        "warning": warning,
        "recommendation": recommendation,
        "top_factors": result["top_factors"], "explanation": result["explanation"],
    }


def message_response(message: str) -> dict:
    result = explain_message(message)
    risk_score = float(result["risk_score"])
    risky = result["prediction"] == 1
    status = result["status"]
    warning = {
        "SAFE": "The model found a low spam probability for this message.",
        "LOW_RISK": "The message has a low spam score; still review links and requests carefully.",
        "SUSPICIOUS": "This message has patterns associated with spam. Review it carefully.",
        "HIGH_RISK": "This message has a high spam score. Avoid links and requests for sensitive information.",
        "DANGEROUS": "This message has a very high spam score. Do not click links or share sensitive information.",
    }[status]
    recommendation = "Continue to be careful with links and requests for sensitive information." if status in {"SAFE", "LOW_RISK"} else "Do not click links or share your OTP, PIN, password, or financial details."
    return {
        "type": "message", "input": message, "prediction": result["label"],
        "label": "Spam / Suspicious" if risky else "Safe / Ham", "risk_score": round(risk_score, 2),
        "spam_probability": result["spam_probability"], "ham_probability": result["ham_probability"],
        "status": status,
        "status_basis": "Risk level is based on the model's spam probability; prediction remains the model's class.",
        "warning": warning,
        "recommendation": recommendation,
        "top_factors": result["top_factors"], "explanation": result["explanation"],
        "dataset_note": read_json(MESSAGE_METADATA_PATH)["dataset_limitation"],
    }


@app.get("/")
def index():
    return render_template("index.html")


@app.get("/api/health")
def health():
    try:
        explain_url("https://example.com")
        explain_message("Hello")
        return jsonify({"status": "ok", "models_loaded": True})
    except Exception:
        app.logger.exception("Model health check failed")
        return jsonify({"status": "unavailable", "models_loaded": False}), 503


@app.get("/api/metrics")
def metrics():
    try:
        return jsonify({"url": read_json(URL_METRICS_PATH), "message": read_json(MESSAGE_METRICS_PATH)})
    except (OSError, json.JSONDecodeError):
        app.logger.exception("Could not load metrics")
        return jsonify({"error": "Model performance information is unavailable."}), 503


def analyze_url_handler():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object containing a URL."}), 400
    url = str(payload.get("url") or "").strip()
    if not url:
        return jsonify({"error": "Please enter a URL first."}), 400
    if not valid_url(url):
        return jsonify({"error": "Please enter a valid URL, such as https://example.com."}), 400
    try:
        return jsonify(url_response(url))
    except Exception:
        app.logger.exception("URL analysis failed")
        return jsonify({"error": "The URL could not be analyzed right now. Please try again."}), 500


def analyze_message_handler():
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return jsonify({"error": "Send a JSON object containing a message."}), 400
    message = str(payload.get("message") or "").strip()
    if not message:
        return jsonify({"error": "Please enter a message first."}), 400
    try:
        return jsonify(message_response(message))
    except Exception:
        app.logger.exception("Message analysis failed")
        return jsonify({"error": "The message could not be analyzed right now. Please try again."}), 500


app.add_url_rule("/api/analyze/url", view_func=analyze_url_handler, methods=["POST"])
app.add_url_rule("/api/analyze/message", view_func=analyze_message_handler, methods=["POST"])
# Preserve original endpoint names for callers of the earlier prototype.
app.add_url_rule("/api/analyze-url", view_func=analyze_url_handler, methods=["POST"])
app.add_url_rule("/api/analyze-message", view_func=analyze_message_handler, methods=["POST"])


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
