from app.trends import calculate_trends


def test_calculate_monthly_trends():
    transactions = [
        {
            "transaction_id": "TX001",
            "timestamp": "2026-08-10T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": 100000,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX002",
            "timestamp": "2026-08-20T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND002",
            "amount": 50000,
            "currency": "INR",
            "description": "Recycling waste management",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX003",
            "timestamp": "2026-09-10T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND003",
            "amount": 75000,
            "currency": "INR",
            "description": "Diesel transportation",
            "sector": "MANUFACTURING",
        },
    ]

    result = calculate_trends(transactions)

    assert len(result) == 2

    assert result[0]["period"] == "2026-08"
    assert result[1]["period"] == "2026-09"

    assert result[0]["transaction_count"] == 2
    assert result[1]["transaction_count"] == 1

    assert "overall_score" in result[0]
    assert "environmental_score" in result[0]
    assert "social_score" in result[0]
    assert "governance_score" in result[0]


def test_trends_are_chronologically_sorted():
    transactions = [
        {
            "transaction_id": "TX001",
            "timestamp": "2026-09-10T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": 100000,
            "currency": "INR",
            "description": "Diesel transportation",
            "sector": "MANUFACTURING",
        },
        {
            "transaction_id": "TX002",
            "timestamp": "2026-07-10T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND002",
            "amount": 50000,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
    ]

    result = calculate_trends(transactions)

    assert result[0]["period"] == "2026-07"
    assert result[1]["period"] == "2026-09"


def test_empty_transactions_return_empty_trends():
    assert calculate_trends([]) == []
    