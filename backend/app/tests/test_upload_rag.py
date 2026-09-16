from fastapi.testclient import TestClient

from app.main import app
from app.rag import retrieve_context
from app.store import clear_transactions
from app.vector_store import clear_collection


client = TestClient(app)


def test_csv_upload_automatically_indexes_report():
    clear_transactions()
    clear_collection()

    csv_content = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX1001,2026-09-01T10:00:00,COMP1000,VEND001,250000,INR,Solar panel procurement,MANUFACTURING
TX1002,2026-09-02T10:00:00,COMP1000,VEND002,2000000,INR,Diesel fuel procurement,MANUFACTURING
"""

    response = client.post(
        "/transactions/upload-csv",
        files={
            "file": (
                "transactions.csv",
                csv_content,
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_count"] == 2
    assert "COMP1000" in data["indexed_companies"]
    assert data["indexed_companies"]["COMP1000"] > 0

    results = retrieve_context(
        "Why is environmental performance affected?",
        "COMP1000",
        n_results=5,
    )

    assert results

    assert all(
        result["metadata"]["company_id"] == "COMP1000"
        for result in results
    )


def test_new_upload_replaces_old_company_index():
    clear_transactions()
    clear_collection()

    first_csv = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX1101,2026-09-01T10:00:00,COMP1100,VEND001,2000000,INR,Diesel fuel procurement,MANUFACTURING
"""

    response = client.post(
        "/transactions/upload-csv",
        files={
            "file": (
                "first.csv",
                first_csv,
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    second_csv = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX1102,2026-09-05T10:00:00,COMP1100,VEND002,300000,INR,Solar panel procurement,MANUFACTURING
"""

    response = client.post(
        "/transactions/upload-csv",
        files={
            "file": (
                "second.csv",
                second_csv,
                "text/csv",
            )
        },
    )

    assert response.status_code == 200

    results = retrieve_context(
        "solar panel procurement",
        "COMP1100",
        n_results=10,
    )

    print("\n=== RAG RESULTS ===")

    for result in results:
        print("ID:", result["id"])
        print("DOCUMENT:", result["document"])
        print("METADATA:", result["metadata"])
        print("DISTANCE:", result["distance"])
        print()

    assert results

    documents = [
        result["document"].lower()
        for result in results
    ]

    assert any(
        "renewable_energy" in document
        for document in documents
    )

    assert not any(
        "diesel" in document
        for document in documents
    )