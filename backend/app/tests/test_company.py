from app.company import build_company_profile


def test_build_company_profile():
    transactions = [
        {
            "transaction_id": "TX001",
            "timestamp": "2026-09-01T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": 250000,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX002",
            "timestamp": "2026-09-05T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND002",
            "amount": 5000000,
            "currency": "INR",
            "description": "Diesel fuel procurement",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX003",
            "timestamp": "2026-09-10T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND003",
            "amount": 10000,
            "currency": "INR",
            "description": "Office stationery purchase",
            "sector": "MANUFACTURING",
        },
    ]

    result = build_company_profile(
        "COMP001",
        transactions,
    )

    assert result["company_id"] == "COMP001"
    assert result["transaction_count"] == 3
    assert result["total_volume"] == 5260000

    assert "environmental_score" in result
    assert "social_score" in result
    assert "governance_score" in result
    assert "overall_score" in result

    assert result["anomaly_count"] == 1
    assert result["high_risk_anomalies"] == 1

    assert result["impact_counts"]["POSITIVE"] == 1
    assert result["impact_counts"]["NEGATIVE"] == 1
    assert result["impact_counts"]["NEUTRAL"] == 1


def test_empty_company_profile():
    result = build_company_profile(
        "COMP001",
        [],
    )

    assert result["company_id"] == "COMP001"
    assert result["transaction_count"] == 0
    assert result["total_volume"] == 0
    assert result["anomaly_count"] == 0
    assert result["high_risk_anomalies"] == 0
    assert result["overall_score"] == 50