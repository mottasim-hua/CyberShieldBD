def risk_level(score: float) -> str:
    if score < 25:
        return "SAFE"
    if score < 50:
        return "LOW_RISK"
    if score < 70:
        return "SUSPICIOUS"
    if score < 85:
        return "HIGH_RISK"
    return "DANGEROUS"