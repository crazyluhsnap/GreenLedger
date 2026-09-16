from app.anomaly import detect_anomaly


def test_fossil_fuel_high_value_transaction_is_anomaly():
    result = detect_anomaly(
        amount=5000000,
        description="Diesel fuel procurement",
        sector="MANUFACTURING",
    )

    assert result["is_anomaly"] is True
    assert result["severity"] == "HIGH"
    assert len(result["reasons"]) > 0


def test_corruption_transaction_is_anomaly():
    result = detect_anomaly(
        amount=100000,
        description="Government official bribery payment",
        sector="FINANCIAL_SERVICES",
    )

    assert result["is_anomaly"] is True
    assert result["severity"] == "HIGH"
    assert "corruption" in result["reasons"][0].lower()


def test_normal_transaction_is_not_anomaly():
    result = detect_anomaly(
        amount=10000,
        description="Office stationery purchase",
        sector="MANUFACTURING",
    )

    assert result["is_anomaly"] is False
    assert result["severity"] == "LOW"
    assert result["reasons"] == []


def test_renewable_transaction_is_not_anomaly():
    result = detect_anomaly(
        amount=500000,
        description="Solar panel procurement",
        sector="MANUFACTURING",
    )

    assert result["is_anomaly"] is False
    assert result["severity"] == "LOW"