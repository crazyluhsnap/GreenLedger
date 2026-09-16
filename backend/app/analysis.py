from app.anomaly import detect_anomaly
from app.scoring import calculate_esg_score
from app.recommendations import generate_recommendations


SIGNAL_EXPLANATIONS = {
    "RENEWABLE_ENERGY": (
        "Transaction supports renewable energy adoption."
    ),
    "FOSSIL_FUEL": (
        "Transaction involves fossil fuel consumption, creating "
        "environmental risk."
    ),
    "RECYCLING": (
        "Transaction supports recycling or waste management."
    ),
    "EMPLOYEE_WELFARE": (
        "Transaction supports employee welfare and workplace safety."
    ),
    "LABOR_RISK": (
        "Transaction indicates potential labor or worker welfare risk."
    ),
    "CORRUPTION": (
        "Transaction contains a corruption-related signal."
    ),
    "COMPLIANCE": (
        "Transaction supports regulatory or internal compliance."
    ),
    "UNCLASSIFIED": (
        "No significant ESG signal detected."
    ),
}


def analyze_transaction(
    description: str,
    sector: str,
    amount: float = 0,
) -> dict:
    result = calculate_esg_score(
        description,
        sector,
    )

    signal = result["signals"][0]

    if signal == "UNCLASSIFIED":
        impact = "NEUTRAL"
    elif any(
        word in signal
        for word in [
            "RISK",
            "CORRUPTION",
            "FOSSIL",
        ]
    ):
        impact = "NEGATIVE"
    else:
        impact = "POSITIVE"

    anomaly = detect_anomaly(
        amount=amount,
        description=description,
        sector=sector,
    )
    
    recommendations = generate_recommendations([signal])

    return {
        **result,
        "impact": impact,
        "reasons": [SIGNAL_EXPLANATIONS[signal]],
        "anomaly": anomaly,
        "recommendations": recommendations,
    }