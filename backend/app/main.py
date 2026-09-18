from fastapi import FastAPI, File, Query, UploadFile, HTTPException

from app.analysis import analyze_transaction
from app.models import Transaction
from app.company import build_company_profile
from app.trends import calculate_trends
from app.csv_loader import load_csv
from app.store import add_transactions, get_company_transactions, get_transactions, replace_company_transactions
from app.report import generate_esg_report
from app.indexer import index_report
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from app.assistant import ask_esg_assistant

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

app = FastAPI(
    title="GreenLedger",
    description="AI-powered ESG intelligence for financial transactions.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    question: str
    n_results: int = 12


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/transactions")
def list_transactions(
    company_id: str | None = None,
    sector: str | None = None,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    transactions = get_transactions()

    if company_id:
        transactions = [
            transaction
            for transaction in transactions
            if transaction.company_id == company_id
        ]

    if sector:
        transactions = [
            transaction
            for transaction in transactions
            if transaction.sector.upper() == sector.upper()
        ]

    total_count = len(transactions)

    paginated_transactions = transactions[
        offset:offset + limit
    ]

    return {
        "transaction_count": total_count,
        "transactions": [
            transaction.model_dump(mode="json")
            for transaction in paginated_transactions
        ],
    }


@app.post("/transactions/analyze")
def analyze(transaction: Transaction):
    result = analyze_transaction(
        transaction.description,
        transaction.sector,
        transaction.amount,
    )

    return {
        "transaction_id": transaction.transaction_id,
        "company_id": transaction.company_id,
        "vendor_id": transaction.vendor_id,
        "amount": transaction.amount,
        "currency": transaction.currency,
        **result,
    }


@app.post("/transactions/analyze/batch")
def analyze_batch(transactions: list[Transaction]):
    results = []

    for transaction in transactions:
        result = analyze_transaction(
            transaction.description,
            transaction.sector,
            transaction.amount,
        )

        results.append(
            {
                "transaction_id": transaction.transaction_id,
                "company_id": transaction.company_id,
                "vendor_id": transaction.vendor_id,
                "amount": transaction.amount,
                "currency": transaction.currency,
                **result,
            }
        )

    return results


@app.get("/companies/{company_id}/profile")
def company_profile(company_id: str):
    transactions = get_company_transactions(company_id)

    if transactions:
        return build_company_profile(company_id, transactions)

    if company_id == "COMP001":
        from app.models import Transaction

        sample_transactions = [
            Transaction(**transaction)
            for transaction in SAMPLE_TRANSACTIONS
        ]

        return build_company_profile(
            company_id,
            sample_transactions,
        )

    return build_company_profile(company_id, [])


@app.get("/companies/{company_id}/trends")
def company_trends(company_id: str):
    transactions = get_company_transactions(company_id)

    if transactions:
        return calculate_trends(transactions)

    if company_id == "COMP001":
        from app.models import Transaction

        sample_transactions = [
            Transaction(**transaction)
            for transaction in SAMPLE_TRANSACTIONS
        ]

        return calculate_trends(sample_transactions)

    return calculate_trends([])

@app.get("/companies/{company_id}/report")
def company_report(company_id: str):
    transactions = get_company_transactions(company_id)

    if transactions:
        report = generate_esg_report(
            company_id,
            transactions,
        )

        indexed_chunks = index_report(report)
        report["indexed_chunks"] = indexed_chunks

        return report

    if company_id == "COMP001":
        from app.models import Transaction

        sample_transactions = [
            Transaction(**transaction)
            for transaction in SAMPLE_TRANSACTIONS
        ]

        report = generate_esg_report(
            company_id,
            sample_transactions,
        )

        indexed_chunks = index_report(report)
        report["indexed_chunks"] = indexed_chunks

        return report

    return generate_esg_report(
        company_id,
        [],
    )
   

@app.post("/transactions/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(
            status_code=400,
            detail="Only CSV files are supported.",
        )

    try:
        content = await file.read()

        import io

        transactions = load_csv(
            io.StringIO(content.decode("utf-8"))
        )

        affected_companies = {
            transaction.company_id
            for transaction in transactions
        }

        for company_id in affected_companies:
            replace_company_transactions(
                company_id,
                transactions,
            )

        indexed_companies = {}

        for company_id in affected_companies:
            company_transactions = get_company_transactions(
            company_id
            )

            report = generate_esg_report(
                company_id,
                company_transactions,
            )

            indexed_companies[company_id] = index_report(report)
        return {
            "transaction_count": len(transactions),
            "indexed_companies": indexed_companies,
            "transactions": [
                transaction.model_dump(mode="json")
                for transaction in transactions
            ],
        }

    except UnicodeDecodeError:
        raise HTTPException(
            status_code=400,
            detail="CSV file must use UTF-8 encoding.",
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )       
        
@app.post("/companies/{company_id}/chat")
def company_chat(
    company_id: str,
    request: ChatRequest,
):
    return ask_esg_assistant(
        question=request.question,
        company_id=company_id,
        n_results=request.n_results,
    )