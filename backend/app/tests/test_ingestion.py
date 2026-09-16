from app.ingestion import load_transactions


def test_load_transactions():
    data = [
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
    ]

    transactions = load_transactions(data)

    assert len(transactions) == 2
    assert transactions[0].transaction_id == "TX001"
    assert transactions[1].amount == 100000


def test_load_transactions_rejects_invalid_transaction():
    data = [
        {
            "transaction_id": "TX001",
            "timestamp": "2026-09-16T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": -100,
            "currency": "INR",
            "description": "Invalid transaction",
            "sector": "MANUFACTURING",
        }
    ]

    try:
        load_transactions(data)
        assert False
    except ValueError:
        assert True