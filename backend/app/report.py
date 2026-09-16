from app.analysis import analyze_transaction
from app.company import build_company_profile
from app.trends import calculate_trends


def generate_esg_report(
    company_id: str,
    transactions: list,
) -> dict:
    profile = build_company_profile(
        company_id,
        transactions,
    )

    trends = calculate_trends(transactions)

    signals = []
    anomalies = []
    recommendations = []

    for transaction in transactions:
        result = analyze_transaction(
            transaction.description
            if hasattr(transaction, "description")
            else transaction["description"],
            transaction.sector
            if hasattr(transaction, "sector")
            else transaction["sector"],
            transaction.amount
            if hasattr(transaction, "amount")
            else transaction["amount"],
        )

        signal = result["signals"][0]

        if signal != "UNCLASSIFIED":
            signals.append({
                "transaction_id": (
                    transaction.transaction_id
                    if hasattr(transaction, "transaction_id")
                    else transaction["transaction_id"]
                ),
                "signal": signal,
                "impact": result["impact"],
                "reason": result["reasons"][0],
            })

        if result["anomaly"]["is_anomaly"]:
            anomalies.append({
                "transaction_id": (
                    transaction.transaction_id
                    if hasattr(transaction, "transaction_id")
                    else transaction["transaction_id"]
                ),
                "severity": result["anomaly"]["severity"],
                "reasons": result["anomaly"]["reasons"],
            })

        for recommendation in result["recommendations"]:
            if recommendation not in recommendations:
                recommendations.append(recommendation)

    return {
        "company_id": company_id,
        "summary": {
            "transaction_count": profile["transaction_count"],
            "total_volume": profile["total_volume"],
            "overall_score": profile["overall_score"],
        },
        "scores": {
            "environmental": profile["environmental_score"],
            "social": profile["social_score"],
            "governance": profile["governance_score"],
        },
        "impact_counts": profile["impact_counts"],
        "trends": trends,
        "key_signals": signals,
        "anomalies": anomalies,
        "recommendations": recommendations,
    }