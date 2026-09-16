from app.report_chunks import report_to_chunks
from app.vector_store import (
    add_documents,
    delete_company_documents,
)


def index_report(report: dict) -> int:
    company_id = report["company_id"]

    delete_company_documents(company_id)

    chunks = report_to_chunks(report)

    if not chunks:
        return 0

    add_documents(
        documents=[
            chunk["text"]
            for chunk in chunks
        ],
        ids=[
            chunk["id"]
            for chunk in chunks
        ],
        metadatas=[
            chunk["metadata"]
            for chunk in chunks
        ],
    )

    return len(chunks)