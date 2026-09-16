from app.analysis import analyze_transaction


def analyze_portfolio(transactions: list[dict]) -> dict:
    if not transactions:
        return {
            "transaction_count": 0,
            "total_volume": 0,
            "environmental_score": 50,
            "social_score": 50,
            "governance_score": 50,
            "overall_score": 50,
            "impact_counts": {
                "POSITIVE": 0,
                "NEGATIVE": 0,
                "NEUTRAL": 0,
            },
        }

    results = []
    total_volume = 0

    for transaction in transactions:
        result = analyze_transaction(
            transaction["description"],
            transaction["sector"],
            transaction["amount"],
        )

        results.append(result)
        total_volume += transaction["amount"]

    count = len(results)

    environmental_score = sum(
        result["environmental_score"]
        for result in results
    ) / count

    social_score = sum(
        result["social_score"]
        for result in results
    ) / count

    governance_score = sum(
        result["governance_score"]
        for result in results
    ) / count

    overall_score = (
        environmental_score
        + social_score
        + governance_score
    ) / 3

    impact_counts = {
        "POSITIVE": 0,
        "NEGATIVE": 0,
        "NEUTRAL": 0,
    }

    for result in results:
        impact_counts[result["impact"]] += 1

    return {
        "transaction_count": count,
        "total_volume": total_volume,
        "environmental_score": environmental_score,
        "social_score": social_score,
        "governance_score": governance_score,
        "overall_score": overall_score,
        "impact_counts": impact_counts,
    }