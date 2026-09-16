from app.models import Transaction


_transactions: list[Transaction] = []


def add_transactions(transactions: list[Transaction]) -> None:
    _transactions.extend(transactions)


def replace_company_transactions(
    company_id: str,
    transactions: list[Transaction],
) -> None:
    global _transactions

    _transactions = [
        transaction
        for transaction in _transactions
        if transaction.company_id != company_id
    ]

    _transactions.extend(
        transaction
        for transaction in transactions
        if transaction.company_id == company_id
    )


def get_transactions() -> list[Transaction]:
    return list(_transactions)


def get_company_transactions(
    company_id: str,
) -> list[Transaction]:
    return [
        transaction
        for transaction in _transactions
        if transaction.company_id == company_id
    ]


def clear_transactions() -> None:
    _transactions.clear()