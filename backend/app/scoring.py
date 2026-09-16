from app.hybrid import classify_transaction_hybrid
from app.sector import get_sector_adjustment


SIGNAL_SCORES = {
    "RENEWABLE_ENERGY": {
        "environmental": 25,
    },
    "FOSSIL_FUEL": {
        "environmental": -25,
    },
    "RECYCLING": {
        "environmental": 20,
    },
    "EMPLOYEE_WELFARE": {
        "social": 25,
    },
    "LABOR_RISK": {
        "social": -30,
    },
    "CORRUPTION": {
        "governance": -35,
    },
    "COMPLIANCE": {
        "governance": 20,
    },
    "UNCLASSIFIED": {},
}


def _clamp_score(score: float) -> float:
    return max(0, min(100, score))


def calculate_esg_score(description: str, sector: str) -> dict:
    classification = classify_transaction_hybrid(description)

    environmental_score = 50.0
    social_score = 50.0
    governance_score = 50.0

    signal = classification["signal"]

    adjustments = SIGNAL_SCORES.get(signal, {})
    sector_adjustment = get_sector_adjustment(sector, signal)

    environmental_score += (
        adjustments.get("environmental", 0)
        * sector_adjustment["environmental"]
    )

    social_score += (
        adjustments.get("social", 0)
        * sector_adjustment["social"]
    )

    governance_score += (
        adjustments.get("governance", 0)
        * sector_adjustment["governance"]
    )

    environmental_score = _clamp_score(environmental_score)
    social_score = _clamp_score(social_score)
    governance_score = _clamp_score(governance_score)

    overall_score = (
        environmental_score
        + social_score
        + governance_score
    ) / 3

    return {
        "environmental_score": environmental_score,
        "social_score": social_score,
        "governance_score": governance_score,
        "overall_score": overall_score,
        "signals": [signal],
        "classification_method": classification["method"],
        "classification_confidence": classification["confidence"],
        "sector": sector,
    }