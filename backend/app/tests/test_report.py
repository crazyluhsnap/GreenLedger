from app.models import Transaction
from app.report import generate_esg_report


def make_transaction(
    transaction_id: str,
    timestamp: str,
    description: str,
    amount: float,
) -> Transaction:
    return Transaction(
        transaction_id=transaction_id,
        timestamp=timestamp,
        company_id="COMP500",
        vendor_id="VEND001",
        amount=amount,
        currency="INR",
        description=description,
        sector="MANUFACTURING",
    )


def test_generate_esg_report():
    transactions = [
        make_transaction(
            "TX501",
            "2026-08-10T10:00:00",
            "Solar panel procurement",
            250000,
        ),
        make_transaction(
            "TX502",
            "2026-08-20T10:00:00",
            "Diesel fuel procurement",
            5000000,
        ),
    ]

    report = generate_esg_report(
        "COMP500",
        transactions,
    )

    assert report["company_id"] == "COMP500"

    assert report["summary"]["transaction_count"] == 2
    assert report["summary"]["total_volume"] == 5250000

    assert "environmental" in report["scores"]
    assert "social" in report["scores"]
    assert "governance" in report["scores"]

    assert len(report["trends"]) == 1
    assert len(report["key_signals"]) == 2


def test_report_contains_anomaly_information():
    transactions = [
        make_transaction(
            "TX503",
            "2026-09-01T10:00:00",
            "Diesel fuel procurement",
            2000000,
        ),
    ]

    report = generate_esg_report(
        "COMP500",
        transactions,
    )

    assert len(report["anomalies"]) == 1
    assert report["anomalies"][0]["transaction_id"] == "TX503"
    assert report["anomalies"][0]["severity"] == "HIGH"


def test_report_contains_recommendations():
    transactions = [
        make_transaction(
            "TX504",
            "2026-09-01T10:00:00",
            "Diesel fuel procurement",
            100000,
        ),
        make_transaction(
            "TX505",
            "2026-09-02T10:00:00",
            "Corruption related payment",
            100000,
        ),
    ]

    report = generate_esg_report(
        "COMP500",
        transactions,
    )

    assert len(report["recommendations"]) >= 2


def test_empty_report():
    report = generate_esg_report(
        "UNKNOWN",
        [],
    )

    assert report["company_id"] == "UNKNOWN"
    assert report["summary"]["transaction_count"] == 0
    assert report["summary"]["total_volume"] == 0
    assert report["scores"]["environmental"] == 50
    assert report["scores"]["social"] == 50
    assert report["scores"]["governance"] == 50
    assert report["trends"] == []
    assert report["key_signals"] == []
    assert report["anomalies"] == []
    assert report["recommendations"] == []