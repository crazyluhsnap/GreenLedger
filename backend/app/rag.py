from app.vector_store import search_documents


def retrieve_context(
    query: str,
    company_id: str,
    n_results: int = 5,
) -> list[dict]:
    if not query.strip():
        return []

    return search_documents(
        query=query,
        company_id=company_id,
        n_results=n_results,
    )


def build_context(
    query: str,
    company_id: str,
    n_results: int = 5,
) -> str:
    results = retrieve_context(
        query=query,
        company_id=company_id,
        n_results=n_results,
    )

    if not results:
        return ""

    context_parts = []

    for index, result in enumerate(results, start=1):
        context_parts.append(
            f"[Evidence {index}]\n"
            f"{result['document']}"
        )

    return "\n\n".join(context_parts)