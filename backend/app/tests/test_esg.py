from app.esg import classify_transaction


def test_solar_transaction_is_environmental():
    result = classify_transaction("Solar panel procurement")

    assert result["category"] == "ENVIRONMENTAL"
    assert result["signal"] == "RENEWABLE_ENERGY"


def test_diesel_transaction_is_environmental_risk():
    result = classify_transaction("Diesel transportation")

    assert result["category"] == "ENVIRONMENTAL"
    assert result["signal"] == "FOSSIL_FUEL"


def test_employee_training_is_social():
    result = classify_transaction("Employee safety training")

    assert result["category"] == "SOCIAL"
    assert result["signal"] == "EMPLOYEE_WELFARE"


def test_bribery_payment_is_governance_risk():
    result = classify_transaction("Government official bribery payment")

    assert result["category"] == "GOVERNANCE"
    assert result["signal"] == "CORRUPTION"


def test_unknown_transaction_returns_neutral():
    result = classify_transaction("Office stationery purchase")

    assert result["category"] == "NEUTRAL"
    assert result["signal"] == "UNCLASSIFIED"
    
    
def test_rule_does_not_match_partial_words():
    result = classify_transaction(
        "Purchase of petroleum products"
    )

    assert result["signal"] == "UNCLASSIFIED"