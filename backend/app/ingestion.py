from app.models import Transaction


def load_transactions(data: list[dict]) -> list[Transaction]:
    transactions = []

    for item in data:
        try:
            transactions.append(Transaction(**item))
        except Exception as exc:
            raise ValueError(f"Invalid transaction: {exc}") from exc

    return transactions