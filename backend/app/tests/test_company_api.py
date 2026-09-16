from fastapi.testclient import TestClient

from app.main import app
from app.store import clear_transactions, add_transactions
from app.models import Transaction


client = TestClient(app)


def make_transaction(
    transaction_id: str,
    company_id: str,
    timestamp: str,
    description: str,
    amount: float,
) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        timestamp=timestamp,
        company_id=company_id,
        vendor_id="VEND001",
        amount=amount,
        currency="INR",
        description=description,
        sector="MANUFACTURING",
    )


def setup_transactions():
    clear_transactions()

    add_transactions([
        make_transaction(
            "TX301",
            "COMP100",
            "2026-08-10T10:00:00",
            "Solar panel procurement",
            250000,
        ),
        make_transaction(
            "TX302",
            "COMP100",
            "2026-08-20T10:00:00",
            "Diesel fuel procurement",
            5000000,
        ),
        make_transaction(
            "TX303",
            "COMP100",
            "2026-09-10T10:00:00",
            "Office stationery purchase",
            10000,
        ),
    ])


def test_company_profile_uses_stored_transactions():
    setup_transactions()

    response = client.get("/companies/COMP100/profile")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "COMP100"
    assert data["transaction_count"] == 3
    assert data["total_volume"] == 5260000


def test_company_trends_uses_stored_transactions():
    setup_transactions()

    response = client.get("/companies/COMP100/trends")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2

    assert data[0]["period"] == "2026-08"
    assert data[0]["transaction_count"] == 2

    assert data[1]["period"] == "2026-09"
    assert data[1]["transaction_count"] == 1


def test_company_profile_returns_empty_for_unknown_company():
    clear_transactions()

    response = client.get("/companies/UNKNOWN/profile")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "UNKNOWN"
    assert data["transaction_count"] == 0
    assert data["total_volume"] == 0
    assert data["overall_score"] == 50


def test_company_trends_returns_empty_for_unknown_company():
    clear_transactions()

    response = client.get("/companies/UNKNOWN/trends")

    assert response.status_code == 200
    assert response.json() == []