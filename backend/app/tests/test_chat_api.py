from fastapi.testclient import TestClient

from app.main import app
from app.vector_store import add_documents, clear_collection


client = TestClient(app)


def setup_vector_data():
    clear_collection()

    add_documents(
        documents=[
            (
                "Company COMP999 environmental performance declined "
                "because of significant fossil fuel spending."
            ),
            (
                "Transaction TX999 involved diesel procurement and "
                "created an environmental risk signal."
            ),
        ],
        ids=[
            "chat_environment",
            "chat_transaction",
        ],
        metadatas=[
            {
                "company_id": "COMP999",
                "section": "environmental",
            },
            {
                "company_id": "COMP999",
                "section": "signals",
                "transaction_id": "TX999",
            },
        ],
    )


def test_chat_endpoint(monkeypatch):
    setup_vector_data()

    def fake_generate_answer(question, context):
        assert question == (
            "Why is environmental performance poor?"
        )
        assert "fossil fuel" in context.lower()

        return (
            "Environmental performance was affected by "
            "fossil fuel spending."
        )

    monkeypatch.setattr(
        "app.assistant.generate_answer",
        fake_generate_answer,
    )

    response = client.post(
        "/companies/COMP999/chat",
        json={
            "question": "Why is environmental performance poor?",
            "n_results": 2,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["answer"] == (
        "Environmental performance was affected by "
        "fossil fuel spending."
    )

    assert len(data["evidence"]) == 2


def test_chat_endpoint_unknown_company():
    setup_vector_data()

    response = client.post(
        "/companies/UNKNOWN/chat",
        json={
            "question": "What is the ESG score?",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["evidence"] == []
    assert "enough ESG evidence" in data["answer"]