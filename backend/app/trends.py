from collections import defaultdict
from datetime import datetime

from app.analysis import analyze_transaction


def _get_value(transaction, field):
    if isinstance(transaction, dict):
        return transaction[field]

    return getattr(transaction, field)


def calculate_trends(transactions: list) -> list[dict]:
    if not transactions:
        return []

    monthly = defaultdict(list)

    for transaction in transactions:
        timestamp = _get_value(transaction, "timestamp")

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)

        month = timestamp.strftime("%Y-%m")
        monthly[month].append(transaction)

    trends = []

    for month in sorted(monthly):
        month_transactions = monthly[month]
        results = []

        for transaction in month_transactions:
            result = analyze_transaction(
                _get_value(transaction, "description"),
                _get_value(transaction, "sector"),
                _get_value(transaction, "amount"),
            )

            results.append(result)

        trends.append({
            "period": month,
            "transaction_count": len(month_transactions),
            "environmental_score": sum(
                result["environmental_score"]
                for result in results
            ) / len(results),
            "social_score": sum(
                result["social_score"]
                for result in results
            ) / len(results),
            "governance_score": sum(
                result["governance_score"]
                for result in results
            ) / len(results),
            "overall_score": sum(
                result["overall_score"]
                for result in results
            ) / len(results),
        })

    return trends