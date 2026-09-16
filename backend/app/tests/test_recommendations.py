from app.recommendations import generate_recommendations


def test_fossil_fuel_recommendation():
    result = generate_recommendations(["FOSSIL_FUEL"])

    assert len(result) == 1
    assert "emission" in result[0].lower()


def test_corruption_recommendation():
    result = generate_recommendations(["CORRUPTION"])

    assert len(result) == 1
    assert "governance" in result[0].lower()


def test_labor_risk_recommendation():
    result = generate_recommendations(["LABOR_RISK"])

    assert len(result) == 1
    assert "labor" in result[0].lower()


def test_multiple_signals_generate_multiple_recommendations():
    result = generate_recommendations(
        ["FOSSIL_FUEL", "CORRUPTION"]
    )

    assert len(result) == 2


def test_positive_signal_has_no_risk_recommendation():
    result = generate_recommendations(["RENEWABLE_ENERGY"])

    assert result == []


def test_unknown_signal_returns_empty_list():
    result = generate_recommendations(["UNKNOWN_SIGNAL"])

    assert result == []