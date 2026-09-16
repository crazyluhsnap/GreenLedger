SECTOR_ADJUSTMENTS = {
    "MANUFACTURING": {
        "FOSSIL_FUEL": {
            "environmental": 1.25,
        },
        "RENEWABLE_ENERGY": {
            "environmental": 1.25,
        },
        "RECYCLING": {
            "environmental": 1.20,
        },
    },
    "ENERGY": {
        "FOSSIL_FUEL": {
            "environmental": 1.50,
        },
        "RENEWABLE_ENERGY": {
            "environmental": 1.40,
        },
    },
    "FINANCIAL_SERVICES": {
        "CORRUPTION": {
            "governance": 1.40,
        },
        "COMPLIANCE": {
            "governance": 1.25,
        },
    },
    "RETAIL": {
        "LABOR_RISK": {
            "social": 1.25,
        },
        "EMPLOYEE_WELFARE": {
            "social": 1.20,
        },
    },
}


def get_sector_adjustment(sector: str, signal: str) -> dict:
    sector_rules = SECTOR_ADJUSTMENTS.get(sector.upper(), {})
    adjustment = sector_rules.get(signal, {})

    return {
        "environmental": adjustment.get("environmental", 1.0),
        "social": adjustment.get("social", 1.0),
        "governance": adjustment.get("governance", 1.0),
    }