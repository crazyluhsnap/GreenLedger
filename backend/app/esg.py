import re


ESG_RULES = {
    "ENVIRONMENTAL": {
        "RENEWABLE_ENERGY": [
            "solar",
            "wind energy",
            "renewable energy",
            "solar panel",
        ],
        "FOSSIL_FUEL": [
            "diesel",
            "petrol",
            "coal",
            "fuel",
            "gasoline",
        ],
        "RECYCLING": [
            "recycling",
            "recycled",
            "waste management",
        ],
    },
    "SOCIAL": {
        "EMPLOYEE_WELFARE": [
            "employee safety",
            "safety training",
            "employee training",
            "health insurance",
            "worker welfare",
        ],
        "LABOR_RISK": [
            "child labor",
            "forced labor",
            "labor violation",
            "unsafe working",
        ],
    },
    "GOVERNANCE": {
        "CORRUPTION": [
            "bribery",
            "bribe",
            "corruption",
            "official bribery",
        ],
        "COMPLIANCE": [
            "compliance audit",
            "regulatory compliance",
            "internal audit",
        ],
    },
}


def _matches_keyword(text: str, keyword: str) -> bool:
    pattern = rf"\b{re.escape(keyword.lower())}\b"
    return bool(re.search(pattern, text))


def classify_transaction(description: str) -> dict:
    text = description.lower()

    for category, signals in ESG_RULES.items():
        for signal, keywords in signals.items():
            for keyword in keywords:
                if _matches_keyword(text, keyword):
                    return {
                        "category": category,
                        "signal": signal,
                    }

    return {
        "category": "NEUTRAL",
        "signal": "UNCLASSIFIED",
    }