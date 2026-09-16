from app.report_chunks import report_to_chunks


def make_report():
    return {
        "company_id": "COMP900",
        "summary": {
            "transaction_count": 3,
            "total_volume": 5250000,
            "overall_score": 48.5,
        },
        "scores": {
            "environmental": 40.0,
            "social": 55.0,
            "governance": 50.5,
        },
        "impact_counts": {
            "POSITIVE": 1,
            "NEGATIVE": 1,
            "NEUTRAL": 1,
        },
        "trends": [
            {
                "period": "2026-09",
                "transaction_count": 3,
                "environmental_score": 40.0,
                "social_score": 55.0,
                "governance_score": 50.5,
                "overall_score": 48.5,
            }
        ],
        "key_signals": [
            {
                "transaction_id": "TX901",
                "signal": "FOSSIL_FUEL",
                "impact": "NEGATIVE",
                "reason": "Transaction involves fossil fuel consumption.",
            }
        ],
        "anomalies": [
            {
                "transaction_id": "TX901",
                "severity": "HIGH",
                "reasons": [
                    "High-value transaction involves fossil fuel activity."
                ],
            }
        ],
        "recommendations": [
            "Consider transitioning transportation and energy spend "
            "toward lower-emission alternatives."
        ],
    }


def test_report_to_chunks_creates_expected_sections():
    chunks = report_to_chunks(make_report())

    sections = {
        chunk["metadata"]["section"]
        for chunk in chunks
    }

    assert "summary" in sections
    assert "scores" in sections
    assert "signals" in sections
    assert "anomalies" in sections
    assert "recommendations" in sections
    assert "trends" in sections


def test_report_chunks_preserve_company_id():
    chunks = report_to_chunks(make_report())

    assert all(
        chunk["metadata"]["company_id"] == "COMP900"
        for chunk in chunks
    )


def test_report_chunks_have_unique_ids():
    chunks = report_to_chunks(make_report())

    ids = [chunk["id"] for chunk in chunks]

    assert len(ids) == len(set(ids))


def test_report_chunks_contain_text():
    chunks = report_to_chunks(make_report())

    assert all(
        isinstance(chunk["text"], str) and chunk["text"]
        for chunk in chunks
    )