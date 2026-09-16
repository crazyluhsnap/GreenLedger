RECOMMENDATIONS = {
    "FOSSIL_FUEL": (
        "Consider transitioning transportation and energy spend "
        "toward lower-emission alternatives."
    ),
    "CORRUPTION": (
        "Review governance controls, approval workflows, and "
        "compliance procedures for this transaction."
    ),
    "LABOR_RISK": (
        "Review supplier labor practices, worker safety, and "
        "employment compliance."
    ),
}


def generate_recommendations(signals: list[str]) -> list[str]:
    recommendations = []

    for signal in signals:
        recommendation = RECOMMENDATIONS.get(signal)

        if recommendation:
            recommendations.append(recommendation)

    return recommendations