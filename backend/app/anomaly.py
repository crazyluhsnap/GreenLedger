from app.esg import classify_transaction


HIGH_RISK_SIGNALS = {
    "FOSSIL_FUEL",
    "CORRUPTION",
    "LABOR_RISK",
}


def detect_anomaly(
    amount: float,
    description: str,
    sector: str,
) -> dict:
    classification = classify_transaction(description)

    signal = classification["signal"]
    reasons = []

    if signal == "CORRUPTION":
        reasons.append(
            "Transaction contains a corruption-related signal."
        )

    elif signal == "FOSSIL_FUEL" and amount >= 1_000_000:
        reasons.append(
            "High-value transaction involves fossil fuel activity."
        )

    elif signal == "LABOR_RISK":
        reasons.append(
            "Transaction contains a potential labor risk signal."
        )

    if signal in HIGH_RISK_SIGNALS and reasons:
        return {
            "is_anomaly": True,
            "severity": "HIGH",
            "reasons": reasons,
        }

    return {
        "is_anomaly": False,
        "severity": "LOW",
        "reasons": [],
    }