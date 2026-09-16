from app.rag import build_context, retrieve_context
from app.vector_store import add_documents, clear_collection


def setup_vector_data():
    clear_collection()

    add_documents(
        documents=[
            (
                "Company COMP700 environmental performance declined "
                "because of significant fossil fuel spending."
            ),
            (
                "Company COMP700 employee safety training improved "
                "the social ESG score."
            ),
            (
                "Company COMP700 governance performance improved "
                "through compliance audits."
            ),
        ],
        ids=[
            "rag_environment",
            "rag_social",
            "rag_governance",
        ],
        metadatas=[
            {
                "company_id": "COMP700",
                "section": "environmental",
            },
            {
                "company_id": "COMP700",
                "section": "social",
            },
            {
                "company_id": "COMP700",
                "section": "governance",
            },
        ],
    )


def test_retrieve_context_returns_relevant_evidence():
    setup_vector_data()

    results = retrieve_context(
        "Why did environmental performance decline?",
        "COMP700",
        n_results=1,
    )

    assert len(results) == 1
    assert results[0]["id"] == "rag_environment"


def test_retrieve_context_respects_company():
    setup_vector_data()

    add_documents(
        documents=[
            "Company COMP701 has strong renewable energy activity."
        ],
        ids=["other_company"],
        metadatas=[
            {
                "company_id": "COMP701",
                "section": "environmental",
            }
        ],
    )

    results = retrieve_context(
        "environmental performance",
        "COMP700",
        n_results=10,
    )

    assert results
    assert all(
        result["metadata"]["company_id"] == "COMP700"
        for result in results
    )


def test_build_context_returns_formatted_evidence():
    setup_vector_data()

    context = build_context(
        "Why is environmental performance poor?",
        "COMP700",
        n_results=1,
    )

    assert "[Evidence 1]" in context
    assert "fossil fuel" in context.lower()


def test_empty_query_returns_no_context():
    setup_vector_data()

    assert retrieve_context(
        "   ",
        "COMP700",
    ) == []

    assert build_context(
        "   ",
        "COMP700",
    ) == ""


def test_unknown_company_returns_no_context():
    setup_vector_data()

    results = retrieve_context(
        "environmental performance",
        "UNKNOWN",
    )

    assert results == []

    context = build_context(
        "environmental performance",
        "UNKNOWN",
    )

    assert context == ""