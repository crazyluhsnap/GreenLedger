from app.analysis import analyze_transaction


def test_renewable_transaction_has_positive_explanation():
    result = analyze_transaction(
        "Solar panel procurement",
        "MANUFACTURING",
    )

    assert result["overall_score"] > 50
    assert result["impact"] == "POSITIVE"
    assert len(result["reasons"]) > 0
    assert "renewable" in result["reasons"][0].lower()


def test_fossil_fuel_transaction_has_negative_explanation():
    result = analyze_transaction(
        "Diesel transportation",
        "MANUFACTURING",
    )

    assert result["impact"] == "NEGATIVE"
    assert len(result["reasons"]) > 0
    assert "fossil" in result["reasons"][0].lower()


def test_corruption_transaction_has_negative_explanation():
    result = analyze_transaction(
        "Government official bribery payment",
        "MANUFACTURING",
    )

    assert result["impact"] == "NEGATIVE"
    assert len(result["reasons"]) > 0
    assert "corruption" in result["reasons"][0].lower()


def test_neutral_transaction_has_neutral_impact():
    result = analyze_transaction(
        "Office stationery purchase",
        "MANUFACTURING",
    )

    assert result["impact"] == "NEUTRAL"
    assert result["reasons"] == [
        "No significant ESG signal detected."
    ]
    
    
def test_full_transaction_analysis_includes_anomaly_detection():
    result = analyze_transaction(
        "Diesel fuel procurement",
        "MANUFACTURING",
        amount=5000000,
    )

    assert "environmental_score" in result
    assert "social_score" in result
    assert "governance_score" in result
    assert "overall_score" in result

    assert "anomaly" in result
    assert result["anomaly"]["is_anomaly"] is True
    assert result["anomaly"]["severity"] == "HIGH"


def test_normal_transaction_has_no_anomaly():
    result = analyze_transaction(
        "Office stationery purchase",
        "MANUFACTURING",
        amount=10000,
    )

    assert result["anomaly"]["is_anomaly"] is False
    assert result["anomaly"]["severity"] == "LOW"
    
def test_analysis_includes_recommendation_for_risky_signal():
    result = analyze_transaction(
        "Diesel fuel procurement",
        "MANUFACTURING",
        amount=5000000,
    )

    assert "recommendations" in result
    assert len(result["recommendations"]) > 0
    assert "emission" in result["recommendations"][0].lower()


def test_analysis_has_no_recommendation_for_neutral_transaction():
    result = analyze_transaction(
        "Office stationery purchase",
        "MANUFACTURING",
        amount=10000,
    )

    assert result["recommendations"] == []