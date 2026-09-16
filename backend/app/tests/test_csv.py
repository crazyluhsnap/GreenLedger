import io

from app.csv_loader import load_csv


VALID_CSV = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX001,2026-09-01T10:00:00,COMP001,VEND001,250000,INR,Solar panel procurement,MANUFACTURING
TX002,2026-09-02T11:00:00,COMP001,VEND002,100000,INR,Diesel transportation,MANUFACTURING
"""


def test_load_csv():
    file = io.StringIO(VALID_CSV)

    transactions = load_csv(file)

    assert len(transactions) == 2
    assert transactions[0].transaction_id == "TX001"
    assert transactions[1].amount == 100000


def test_load_csv_preserves_transaction_fields():
    file = io.StringIO(VALID_CSV)

    transactions = load_csv(file)

    assert transactions[0].company_id == "COMP001"
    assert transactions[0].vendor_id == "VEND001"
    assert transactions[0].currency == "INR"
    assert transactions[0].sector == "MANUFACTURING"


def test_load_csv_rejects_invalid_transaction():
    csv_data = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX001,2026-09-01T10:00:00,COMP001,VEND001,-100,INR,Invalid transaction,MANUFACTURING
"""

    file = io.StringIO(csv_data)

    try:
        load_csv(file)
        assert False
    except ValueError:
        assert True


def test_load_csv_rejects_missing_column():
    csv_data = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description
TX001,2026-09-01T10:00:00,COMP001,VEND001,100000,INR,Solar panel procurement
"""

    file = io.StringIO(csv_data)

    try:
        load_csv(file)
        assert False
    except ValueError:
        assert True