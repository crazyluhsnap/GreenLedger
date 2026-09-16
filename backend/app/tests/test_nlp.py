from app.nlp import classify_with_nlp


def test_nlp_classifies_renewable_energy():
    result = classify_with_nlp(
        "Installation of photovoltaic generation equipment"
    )

    assert result["signal"] == "RENEWABLE_ENERGY"


def test_nlp_classifies_fossil_fuel():
    result = classify_with_nlp(
        "Purchase of diesel fuel for company vehicles"
    )

    assert result["signal"] == "FOSSIL_FUEL"


def test_nlp_classifies_employee_welfare():
    result = classify_with_nlp(
        "Workplace safety and employee training program"
    )

    assert result["signal"] == "EMPLOYEE_WELFARE"


def test_nlp_classifies_corruption():
    result = classify_with_nlp(
        "Illegal payment to government official"
    )

    assert result["signal"] == "CORRUPTION"


def test_nlp_returns_confidence():
    result = classify_with_nlp(
        "Purchase of renewable energy equipment"
    )

    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1