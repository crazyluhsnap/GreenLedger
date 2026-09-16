from app.models import Transaction
from app.store import (
    add_transactions,
    clear_transactions,
    get_company_transactions,
    get_transactions,
    replace_company_transactions,
)


def make_transaction(transaction_id: str, company_id: str) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        timestamp="2026-09-01T10:00:00",
        company_id=company_id,
        vendor_id="VEND001",
        amount=100000,
        currency="INR",
        description="Solar panel procurement",
        sector="MANUFACTURING",
    )


def test_add_and_get_transactions():
    clear_transactions()

    transactions = [
        make_transaction("TX001", "COMP001"),
        make_transaction("TX002", "COMP001"),
    ]

    add_transactions(transactions)

    result = get_transactions()

    assert len(result) == 2
    assert result[0].transaction_id == "TX001"
    assert result[1].transaction_id == "TX002"


def test_get_company_transactions():
    clear_transactions()

    add_transactions([
        make_transaction("TX001", "COMP001"),
        make_transaction("TX002", "COMP002"),
        make_transaction("TX003", "COMP001"),
    ])

    result = get_company_transactions("COMP001")

    assert len(result) == 2
    assert result[0].transaction_id == "TX001"
    assert result[1].transaction_id == "TX003"


def test_get_company_transactions_returns_empty_for_unknown_company():
    clear_transactions()

    add_transactions([
        make_transaction("TX001", "COMP001"),
    ])

    result = get_company_transactions("UNKNOWN")

    assert result == []
    

def test_replace_company_transactions():
    clear_transactions()

    first = Transaction(
        transaction_id="TX1",
        timestamp="2026-09-01T10:00:00",
        company_id="COMP1",
        vendor_id="VEND1",
        amount=100000,
        currency="INR",
        description="Diesel fuel procurement",
        sector="MANUFACTURING",
    )

    second = Transaction(
        transaction_id="TX2",
        timestamp="2026-09-02T10:00:00",
        company_id="COMP1",
        vendor_id="VEND2",
        amount=200000,
        currency="INR",
        description="Solar panel procurement",
        sector="MANUFACTURING",
    )

    add_transactions([first])

    replace_company_transactions(
        "COMP1",
        [second],
    )

    transactions = get_company_transactions("COMP1")

    assert len(transactions) == 1
    assert transactions[0].transaction_id == "TX2"