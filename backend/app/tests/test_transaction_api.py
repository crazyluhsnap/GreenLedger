from fastapi.testclient import TestClient

from app.main import app
from app.models import Transaction
from app.store import add_transactions, clear_transactions


client = TestClient(app)


def make_transaction(
    transaction_id: str,
    company_id: str,
    sector: str,
) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        timestamp="2026-09-01T10:00:00",
        company_id=company_id,
        vendor_id="VEND001",
        amount=100000,
        currency="INR",
        description="Solar panel procurement",
        sector=sector,
    )


def setup_transactions():
    clear_transactions()

    add_transactions([
        make_transaction("TX401", "COMP001", "MANUFACTURING"),
        make_transaction("TX402", "COMP001", "ENERGY"),
        make_transaction("TX403", "COMP002", "RETAIL"),
    ])


def test_get_transactions():
    setup_transactions()

    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 3
    assert len(data["transactions"]) == 3
    assert data["transactions"][0]["transaction_id"] == "TX401"


def test_get_transactions_by_company():
    setup_transactions()

    response = client.get("/transactions?company_id=COMP001")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 2

    ids = [
        transaction["transaction_id"]
        for transaction in data["transactions"]
    ]

    assert ids == ["TX401", "TX402"]


def test_get_transactions_by_sector():
    setup_transactions()

    response = client.get("/transactions?sector=RETAIL")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 1
    assert data["transactions"][0]["transaction_id"] == "TX403"


def test_get_transactions_with_pagination():
    setup_transactions()

    response = client.get("/transactions?limit=1&offset=1")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 3
    assert len(data["transactions"]) == 1
    assert data["transactions"][0]["transaction_id"] == "TX402"


def test_get_transactions_empty():
    clear_transactions()

    response = client.get("/transactions")

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 0
    assert data["transactions"] == []