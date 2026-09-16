from app.vector_store import (
    add_documents,
    clear_collection,
    search_documents,
    delete_company_documents,
)


def test_add_and_search_documents():
    clear_collection()

    add_documents(
        documents=[
            "The environmental score decreased because of fossil fuel spending.",
            "Employee safety training improved the social score.",
            "Governance controls were strengthened through compliance audits.",
        ],
        ids=[
            "test_environment",
            "test_social",
            "test_governance",
        ],
        metadatas=[
            {
                "company_id": "TEST001",
                "section": "environmental",
            },
            {
                "company_id": "TEST001",
                "section": "social",
            },
            {
                "company_id": "TEST001",
                "section": "governance",
            },
        ],
    )

    results = search_documents(
        "Why is environmental performance poor?",
        company_id="TEST001",
        n_results=1,
    )

    assert len(results) == 1
    assert results[0]["id"] == "test_environment"


def test_search_filters_by_company():
    clear_collection()

    add_documents(
        documents=[
            "Company A has significant fossil fuel expenditure.",
            "Company B has significant renewable energy expenditure.",
        ],
        ids=[
            "company_a",
            "company_b",
        ],
        metadatas=[
            {
                "company_id": "A",
                "section": "environmental",
            },
            {
                "company_id": "B",
                "section": "environmental",
            },
        ],
    )

    results = search_documents(
        "environmental spending",
        company_id="A",
        n_results=5,
    )

    assert len(results) == 1
    assert results[0]["id"] == "company_a"


def test_empty_search():
    clear_collection()

    results = search_documents(
        "anything",
        company_id="UNKNOWN",
        n_results=5,
    )

    assert results == []
    
    
def test_delete_company_documents():
    clear_collection()

    add_documents(
        documents=[
            "Company A has fossil fuel spending.",
            "Company B has renewable energy spending.",
        ],
        ids=[
            "delete_a",
            "delete_b",
        ],
        metadatas=[
            {
                "company_id": "A",
                "section": "environmental",
            },
            {
                "company_id": "B",
                "section": "environmental",
            },
        ],
    )

    delete_company_documents("A")

    results_a = search_documents(
        "environmental spending",
        company_id="A",
        n_results=5,
    )

    results_b = search_documents(
        "environmental spending",
        company_id="B",
        n_results=5,
    )

    assert results_a == []
    assert len(results_b) == 1
    assert results_b[0]["id"] == "delete_b"