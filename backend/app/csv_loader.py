import csv


from app.models import Transaction


REQUIRED_COLUMNS = {
    "transaction_id",
    "timestamp",
    "company_id",
    "vendor_id",
    "amount",
    "currency",
    "description",
    "sector",
}


def load_csv(file) -> list[Transaction]:
    reader = csv.DictReader(file)

    if reader.fieldnames is None:
        raise ValueError("CSV file is empty or has no header.")

    missing_columns = REQUIRED_COLUMNS - set(reader.fieldnames)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {sorted(missing_columns)}"
        )

    transactions = []

    for row_number, row in enumerate(reader, start=2):
        try:
            transactions.append(Transaction(**row))
        except Exception as exc:
            raise ValueError(
                f"Invalid transaction at CSV row {row_number}: {exc}"
            ) from exc

    return transactions