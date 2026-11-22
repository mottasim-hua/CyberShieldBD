from app import app
from ml.risk_levels import risk_level
from ml.url_detection.xai import explain_url
from ml.message_detection.xai import explain_message

URL_CASES = [
	("legitimate", "https://www.google.com/"),
	("legitimate", "https://www.microsoft.com/"),
	("legitimate", "https://www.apple.com/"),
	("legitimate", "https://www.wikipedia.org/"),
	("legitimate", "https://www.python.org/"),
	("suspicious", "http://secure-account-verify.example.com/login"),
	("suspicious", "http://bank-security-alert.example.com/update"),
	("suspicious", "http://account-suspended.example.com/restore"),
	("suspicious", "http://free-prize-winner.example.com/claim"),
	("suspicious", "http://urgent-password-reset.example.com/account"),
]

MESSAGE_CASES = [
	("legitimate", "Hey, are we still meeting for lunch at noon?"),
	("legitimate", "Can you send me the notes from today's lecture?"),
	("legitimate", "I'm on my way home, see you soon."),
	("legitimate", "Please call me when you get a chance."),
	("legitimate", "Your appointment is confirmed for 3 pm tomorrow."),
	("suspicious", "Congratulations! You have won a free prize. Call now to claim."),
	("suspicious", "URGENT! Your account is suspended. Verify your password immediately at this link."),
	("suspicious", "Free entry in a weekly competition to win a 1000 prize. Text WIN now!"),
	("suspicious", "Your bank account is locked. Reply with your PIN and OTP to restore access."),
	("suspicious", "Claim your cash reward now! Click here and enter your details."),
]


def test_risk_level_boundaries():
	cases = {
		0: "SAFE", 24.99: "SAFE", 25: "LOW_RISK", 49.99: "LOW_RISK",
		50: "SUSPICIOUS", 69.99: "SUSPICIOUS", 70: "HIGH_RISK",
		84.99: "HIGH_RISK", 85: "DANGEROUS", 100: "DANGEROUS",
	}
	for score, expected in cases.items():
		assert risk_level(score) == expected


def main():
	test_risk_level_boundaries()
	client = app.test_client()
	for detector, cases, explain, probability_key in (
		("URL", URL_CASES, explain_url, "phishing_probability"),
		("MESSAGE", MESSAGE_CASES, explain_message, "spam_probability"),
	):
		for category, value in cases:
			result = explain(value)
			probability = result[probability_key]
			assert result["risk_score"] == probability
			expected_status = (
				"SAFE" if result["prediction"] == 1
				else "DANGEROUS" if result["risk_score"] >= 80
				else "SUSPICIOUS"
			) if detector == "URL" else risk_level(result["risk_score"])
			assert result["status"] == expected_status
			endpoint, field = ("/api/analyze/url", "url") if detector == "URL" else ("/api/analyze/message", "message")
			response = client.post(endpoint, json={field: value})
			api_result = response.get_json()
			assert response.status_code == 200
			assert api_result["risk_score"] == result["risk_score"]
			assert api_result["status"] == result["status"]
			assert api_result[probability_key] == probability
			print(f"{detector} | {category} | input={value} | predicted_class={result['prediction']} | model_probability={probability:.6f}% | risk_score={result['risk_score']:.6f}% | risk_level={result['status']}")
	print("Risk-band and 20 detector checks passed.")


if __name__=="__main__": main()
