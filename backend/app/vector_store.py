import chromadb

from app.embeddings import get_embedding_function


_client = chromadb.Client()

_collection = _client.get_or_create_collection(
    name="greenledger_reports",
    embedding_function=get_embedding_function(),
)


def add_documents(
    documents: list[str],
    ids: list[str],
    metadatas: list[dict],
) -> None:
    if not documents:
        return

    _collection.upsert(
        documents=documents,
        ids=ids,
        metadatas=metadatas,
    )


def search_documents(
    query: str,
    company_id: str | None = None,
    n_results: int = 5,
) -> list[dict]:
    where = None

    if company_id:
        where = {
            "company_id": company_id,
        }

    results = _collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]
    distances = results.get("distances", [[]])[0]
    ids = results.get("ids", [[]])[0]

    return [
        {
            "id": document_id,
            "document": document,
            "metadata": metadata,
            "distance": distance,
        }
        for document_id, document, metadata, distance in zip(
            ids,
            documents,
            metadatas,
            distances,
        )
    ]


def delete_company_documents(company_id: str) -> None:
    results = _collection.get(
        where={
            "company_id": company_id,
        }
    )

    ids = results.get("ids", [])

    if ids:
        _collection.delete(ids=ids)


def clear_collection() -> None:
    global _collection

    _client.delete_collection("greenledger_reports")

    _collection = _client.get_or_create_collection(
        name="greenledger_reports",
        embedding_function=get_embedding_function(),
    )