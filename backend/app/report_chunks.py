def report_to_chunks(report: dict) -> list[dict]:
    company_id = report["company_id"]
    chunks = []

    summary = report["summary"]

    chunks.append({
        "id": f"{company_id}_summary",
        "text": (
            f"Company {company_id} has {summary['transaction_count']} "
            f"transactions with a total transaction volume of "
            f"{summary['total_volume']}. "
            f"The overall ESG score is "
            f"{summary['overall_score']:.2f}."
        ),
        "metadata": {
            "company_id": company_id,
            "section": "summary",
            "source": "esg_report",
        },
    })

    scores = report["scores"]

    chunks.append({
        "id": f"{company_id}_scores",
        "text": (
            f"Company {company_id} has an environmental ESG score of "
            f"{scores['environmental']:.2f}, a social ESG score of "
            f"{scores['social']:.2f}, and a governance ESG score of "
            f"{scores['governance']:.2f}."
        ),
        "metadata": {
            "company_id": company_id,
            "section": "scores",
            "source": "esg_report",
        },
    })

    for index, signal in enumerate(report["key_signals"]):
        chunks.append({
            "id": f"{company_id}_signal_{index}",
            "text": (
                f"Transaction {signal['transaction_id']} has the ESG "
                f"signal {signal['signal']} with {signal['impact']} "
                f"impact. Reason: {signal['reason']}"
            ),
            "metadata": {
                "company_id": company_id,
                "section": "signals",
                "source": "esg_report",
                "transaction_id": signal["transaction_id"],
            },
        })

    for index, anomaly in enumerate(report["anomalies"]):
        chunks.append({
            "id": f"{company_id}_anomaly_{index}",
            "text": (
                f"Transaction {anomaly['transaction_id']} has a "
                f"{anomaly['severity']} severity ESG anomaly. "
                f"Reasons: {' '.join(anomaly['reasons'])}"
            ),
            "metadata": {
                "company_id": company_id,
                "section": "anomalies",
                "source": "esg_report",
                "transaction_id": anomaly["transaction_id"],
            },
        })

    for index, recommendation in enumerate(
        report["recommendations"]
    ):
        chunks.append({
            "id": f"{company_id}_recommendation_{index}",
            "text": (
                f"ESG recommendation for {company_id}: "
                f"{recommendation}"
            ),
            "metadata": {
                "company_id": company_id,
                "section": "recommendations",
                "source": "esg_report",
            },
        })

    for trend in report["trends"]:
        chunks.append({
            "id": f"{company_id}_trend_{trend['period']}",
            "text": (
                f"For {company_id}, the ESG trend for "
                f"{trend['period']} shows an environmental score of "
                f"{trend['environmental_score']:.2f}, a social score of "
                f"{trend['social_score']:.2f}, a governance score of "
                f"{trend['governance_score']:.2f}, and an overall score "
                f"of {trend['overall_score']:.2f} across "
                f"{trend['transaction_count']} transactions."
            ),
            "metadata": {
                "company_id": company_id,
                "section": "trends",
                "source": "esg_report",
                "period": trend["period"],
            },
        })

    return chunks