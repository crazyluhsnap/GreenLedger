from app.hybrid import classify_transaction_hybrid


def test_rule_engine_takes_priority():
    result = classify_transaction_hybrid(
        "Solar panel procurement"
    )

    assert result["signal"] == "RENEWABLE_ENERGY"
    assert result["method"] == "RULE"


def test_nlp_handles_unseen_wording():
    result = classify_transaction_hybrid(
        "Installation of photovoltaic generation equipment"
    )

    assert result["signal"] == "RENEWABLE_ENERGY"
    assert result["method"] == "NLP"


def test_nlp_handles_unseen_fuel_wording():
    result = classify_transaction_hybrid(
        "Purchase of petroleum products for company vehicles"
    )

    assert result["signal"] == "FOSSIL_FUEL"
    assert result["method"] == "NLP"


def test_result_contains_confidence():
    result = classify_transaction_hybrid(
        "Purchase of renewable energy equipment"
    )

    assert "confidence" in result
    assert 0 <= result["confidence"] <= 1


def test_unknown_description_is_handled():
    result = classify_transaction_hybrid(
        "Quarterly administrative expense"
    )

    assert "signal" in result
    assert "method" in result