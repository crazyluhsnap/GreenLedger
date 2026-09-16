from app.assistant import ask_esg_assistant
from app.vector_store import add_documents, clear_collection


def setup_vector_data():
    clear_collection()

    add_documents(
        documents=[
            (
                "Company COMP800 environmental score declined "
                "because of significant fossil fuel spending."
            ),
            (
                "Transaction TX801 involved diesel fuel procurement "
                "and created an environmental risk signal."
            ),
        ],
        ids=[
            "assistant_environment",
            "assistant_transaction",
        ],
        metadatas=[
            {
                "company_id": "COMP800",
                "section": "environmental",
            },
            {
                "company_id": "COMP800",
                "section": "signals",
                "transaction_id": "TX801",
            },
        ],
    )


def test_assistant_returns_answer_and_evidence(monkeypatch):
    setup_vector_data()

    def fake_generate_answer(question, context):
        assert question == "Why is environmental performance poor?"
        assert "fossil fuel" in context.lower()

        return "Environmental performance was affected by fossil fuel spending."

    monkeypatch.setattr(
        "app.assistant.generate_answer",
        fake_generate_answer,
    )

    result = ask_esg_assistant(
        "Why is environmental performance poor?",
        "COMP800",
    )

    assert "answer" in result
    assert "evidence" in result

    assert result["answer"] == (
        "Environmental performance was affected by fossil fuel spending."
    )

    assert len(result["evidence"]) > 0


def test_assistant_returns_no_evidence_for_unknown_company():
    setup_vector_data()

    result = ask_esg_assistant(
        "What is the environmental score?",
        "UNKNOWN",
    )

    assert result["evidence"] == []
    assert "enough ESG evidence" in result["answer"]


def test_assistant_preserves_evidence_metadata(monkeypatch):
    setup_vector_data()

    monkeypatch.setattr(
        "app.assistant.generate_answer",
        lambda question, context: "Test answer",
    )

    result = ask_esg_assistant(
        "What caused environmental risk?",
        "COMP800",
    )

    assert all(
        "metadata" in evidence
        for evidence in result["evidence"]
    )

    assert any(
        evidence["metadata"]["company_id"] == "COMP800"
        for evidence in result["evidence"]
    )