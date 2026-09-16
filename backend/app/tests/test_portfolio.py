from app.portfolio import analyze_portfolio


def test_analyze_portfolio():
    transactions = [
        {
            "transaction_id": "TX001",
            "timestamp": "2026-09-16T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": 250000,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX002",
            "timestamp": "2026-09-16T11:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND002",
            "amount": 100000,
            "currency": "INR",
            "description": "Diesel transportation",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX003",
            "timestamp": "2026-09-16T12:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND003",
            "amount": 50000,
            "currency": "INR",
            "description": "Office stationery purchase",
            "sector": "MANUFACTURING",
        },
    ]

    result = analyze_portfolio(transactions)

    assert result["transaction_count"] == 3
    assert result["total_volume"] == 400000

    assert "environmental_score" in result
    assert "social_score" in result
    assert "governance_score" in result
    assert "overall_score" in result

    assert result["impact_counts"]["POSITIVE"] == 1
    assert result["impact_counts"]["NEGATIVE"] == 1
    assert result["impact_counts"]["NEUTRAL"] == 1


def test_empty_portfolio():
    result = analyze_portfolio([])

    assert result["transaction_count"] == 0
    assert result["total_volume"] == 0
    assert result["environmental_score"] == 50
    assert result["social_score"] == 50
    assert result["governance_score"] == 50
    assert result["overall_score"] == 50