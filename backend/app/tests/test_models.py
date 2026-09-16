import pytest
from pydantic import ValidationError
from app.models import Transaction

def test_valid_transaction():
    transaction=Transaction(
        transaction_id="TX001",
        timestamp="2026-09-16T10:00:00",
        company_id="COMP001",
        vendor_id="VEND001",
        amount=250000,
        currency="INR",
        description="Solar panel procurement",
        sector="MANUFACTURE",
    )
    assert transaction.transaction_id=="TX001"
    assert transaction.amount==250000
    assert transaction.currency=="INR"
    
def test_transaction_amount_must_be_positive():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TX001",
            timestamp="2026-09-16T10:00:00",
            company_id="COMP001",
            vendor_id="VEND001",
            amount=0,
            currency="INR",
            description="Solar panel procurement",
            sector="MANUFACTURING",
        )


def test_currency_must_be_three_uppercase_letters():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="TX001",
            timestamp="2026-09-16T10:00:00",
            company_id="COMP001",
            vendor_id="VEND001",
            amount=10000,
            currency="inr",
            description="Solar panel procurement",
            sector="MANUFACTURING",
        )


def test_transaction_ids_cannot_be_empty():
    with pytest.raises(ValidationError):
        Transaction(
            transaction_id="",
            timestamp="2026-09-16T10:00:00",
            company_id="COMP001",
            vendor_id="VEND001",
            amount=10000,
            currency="INR",
            description="Solar panel procurement",
            sector="MANUFACTURING",
        )