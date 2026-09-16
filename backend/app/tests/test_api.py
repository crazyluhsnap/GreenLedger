from fastapi.testclient import TestClient

from app.main import app

client=TestClient(app)

def test_health():
    response=client.get("/health")
    
    assert response.status_code==200
    assert response.json()=={
        "status":"ok"
    }
    
    
def test_analyze_transaction():
    response = client.post(
        "/transactions/analyze",
        json={
            "transaction_id": "TX001",
            "timestamp": "2026-09-16T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": 250000,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["transaction_id"] == "TX001"
    assert data["environmental_score"] > 50
    assert data["impact"] == "POSITIVE"
    assert len(data["reasons"]) > 0


def test_analyze_transaction_rejects_invalid_amount():
    response = client.post(
        "/transactions/analyze",
        json={
            "transaction_id": "TX001",
            "timestamp": "2026-09-16T10:00:00",
            "company_id": "COMP001",
            "vendor_id": "VEND001",
            "amount": -100,
            "currency": "INR",
            "description": "Solar panel procurement",
            "sector": "MANUFACTURING",
        },
    )

    assert response.status_code == 422


def test_batch_analyze_transactions():
    response = client.post(
        "/transactions/analyze/batch",
        json=[
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
        ],
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["transaction_id"] == "TX001"
    assert data[1]["transaction_id"] == "TX002"
    
SAMPLE_TRANSACTIONS = [
    {
        "transaction_id": "TX001",
        "timestamp": "2026-08-10T10:00:00",
        "company_id": "COMP001",
        "vendor_id": "VEND001",
        "amount": 250000,
        "currency": "INR",
        "description": "Solar panel procurement",
        "sector": "MANUFACTURING",
    },
    {
        "transaction_id": "TX002",
        "timestamp": "2026-08-20T10:00:00",
        "company_id": "COMP001",
        "vendor_id": "VEND002",
        "amount": 5000000,
        "currency": "INR",
        "description": "Diesel fuel procurement",
        "sector": "MANUFACTURING",
    },
    {
        "transaction_id": "TX003",
        "timestamp": "2026-09-10T10:00:00",
        "company_id": "COMP001",
        "vendor_id": "VEND003",
        "amount": 10000,
        "currency": "INR",
        "description": "Office stationery purchase",
        "sector": "MANUFACTURING",
    },
]


def test_company_profile():
    response = client.get("/companies/COMP001/profile")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "COMP001"
    assert data["transaction_count"] == 3
    assert data["total_volume"] == 5260000
    assert data["anomaly_count"] == 1


def test_company_trends():
    response = client.get("/companies/COMP001/trends")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 2
    assert data[0]["period"] == "2026-08"
    assert data[1]["period"] == "2026-09"


def test_unknown_company_returns_empty_profile():
    response = client.get("/companies/UNKNOWN/profile")

    assert response.status_code == 200

    data = response.json()

    assert data["company_id"] == "UNKNOWN"
    assert data["transaction_count"] == 0


def test_unknown_company_returns_empty_trends():
    response = client.get("/companies/UNKNOWN/trends")

    assert response.status_code == 200
    assert response.json() == []
    
    
def test_upload_csv():
    csv_content = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX101,2026-09-01T10:00:00,COMP002,VEND001,250000,INR,Solar panel procurement,MANUFACTURING
TX102,2026-09-02T11:00:00,COMP002,VEND002,100000,INR,Diesel transportation,MANUFACTURING
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
    assert data["transactions"][0]["transaction_id"] == "TX101"
    assert data["transactions"][1]["transaction_id"] == "TX102"


def test_upload_csv_rejects_invalid_file():
    response = client.post(
        "/transactions/upload-csv",
        files={
            "file": (
                "transactions.csv",
                "invalid,csv\n1,2",
                "text/csv",
            )
        },
    )

    assert response.status_code == 400
    
def test_upload_csv_persists_transactions():
    from app.store import clear_transactions, get_company_transactions

    clear_transactions()

    csv_content = """transaction_id,timestamp,company_id,vendor_id,amount,currency,description,sector
TX201,2026-09-01T10:00:00,COMP003,VEND001,250000,INR,Solar panel procurement,MANUFACTURING
TX202,2026-09-02T11:00:00,COMP003,VEND002,100000,INR,Diesel transportation,MANUFACTURING
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

    stored = get_company_transactions("COMP003")

    assert len(stored) == 2
    assert stored[0].transaction_id == "TX201"
    assert stored[1].transaction_id == "TX202"