from app.indexer import index_report
from app.vector_store import clear_collection, search_documents


def make_report():
    return {
        "company_id": "COMP950",
        "summary": {
            "transaction_count": 2,
            "total_volume": 5250000,
            "overall_score": 45.0,
        },
        "scores": {
            "environmental": 35.0,
            "social": 55.0,
            "governance": 45.0,
        },
        "impact_counts": {
            "POSITIVE": 1,
            "NEGATIVE": 1,
            "NEUTRAL": 0,
        },
        "trends": [
            {
                "period": "2026-09",
                "transaction_count": 2,
                "environmental_score": 35.0,
                "social_score": 55.0,
                "governance_score": 45.0,
                "overall_score": 45.0,
            }
        ],
        "key_signals": [
            {
                "transaction_id": "TX951",
                "signal": "FOSSIL_FUEL",
                "impact": "NEGATIVE",
                "reason": (
                    "Transaction involves fossil fuel consumption."
                ),
            }
        ],
        "anomalies": [],
        "recommendations": [
            (
                "Consider transitioning transportation and energy "
                "spend toward lower-emission alternatives."
            )
        ],
    }


def test_index_report():
    clear_collection()

    count = index_report(make_report())

    assert count > 0

    results = search_documents(
        "environmental fossil fuel performance",
        company_id="COMP950",
        n_results=5,
    )

    assert results


def test_indexed_report_contains_company_metadata():
    clear_collection()

    index_report(make_report())

    results = search_documents(
        "ESG score",
        company_id="COMP950",
        n_results=5,
    )

    assert results

    assert all(
        result["metadata"]["company_id"] == "COMP950"
        for result in results
    )