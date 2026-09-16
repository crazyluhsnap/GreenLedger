from app.analysis import analyze_transaction


def _get_value(transaction, field):
    if isinstance(transaction, dict):
        return transaction[field]

    return getattr(transaction, field)


def build_company_profile(
    company_id: str,
    transactions: list,
) -> dict:
    if not transactions:
        return {
            "company_id": company_id,
            "transaction_count": 0,
            "total_volume": 0,
            "environmental_score": 50,
            "social_score": 50,
            "governance_score": 50,
            "overall_score": 50,
            "anomaly_count": 0,
            "high_risk_anomalies": 0,
            "impact_counts": {
                "POSITIVE": 0,
                "NEGATIVE": 0,
                "NEUTRAL": 0,
            },
        }

    results = []
    total_volume = 0

    for transaction in transactions:
        description = _get_value(transaction, "description")
        sector = _get_value(transaction, "sector")
        amount = _get_value(transaction, "amount")

        result = analyze_transaction(
            description,
            sector,
            amount,
        )

        results.append(result)
        total_volume += amount

    environmental_score = sum(
        result["environmental_score"] for result in results
    ) / len(results)

    social_score = sum(
        result["social_score"] for result in results
    ) / len(results)

    governance_score = sum(
        result["governance_score"] for result in results
    ) / len(results)

    overall_score = sum(
        result["overall_score"] for result in results
    ) / len(results)

    anomaly_count = sum(
        result["anomaly"]["is_anomaly"]
        for result in results
    )

    high_risk_anomalies = sum(
        result["anomaly"]["severity"] == "HIGH"
        for result in results
    )

    impact_counts = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "NEUTRAL": 0,
    }

    for result in results:
        impact_counts[result["impact"]] += 1

    return {
        "company_id": company_id,
        "transaction_count": len(transactions),
        "total_volume": total_volume,
        "environmental_score": environmental_score,
        "social_score": social_score,
        "governance_score": governance_score,
        "overall_score": overall_score,
        "anomaly_count": anomaly_count,
        "high_risk_anomalies": high_risk_anomalies,
        "impact_counts": impact_counts,
    }