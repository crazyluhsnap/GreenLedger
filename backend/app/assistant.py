from app.llm import generate_answer
from app.rag import retrieve_context


def ask_esg_assistant(
    question: str,
    company_id: str,
    n_results: int = 12,
) -> dict:
    results = retrieve_context(
        query=question,
        company_id=company_id,
        n_results=n_results,
    )

    if not results:
        return {
            "answer": (
                "I don't have enough ESG evidence to answer "
                "that question."
            ),
            "evidence": [],
        }

    context = "\n\n".join(
        result["document"]
        for result in results
    )

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "evidence": [
            {
                "id": result["id"],
                "document": result["document"],
                "metadata": result["metadata"],
            }
            for result in results
        ],
    }