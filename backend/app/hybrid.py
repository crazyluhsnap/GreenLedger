from app.esg import classify_transaction
from app.nlp import classify_with_nlp


NLP_CONFIDENCE_THRESHOLD = 0.45


def classify_transaction_hybrid(description: str) -> dict:
    rule_result = classify_transaction(description)

    if rule_result["signal"] != "UNCLASSIFIED":
        return {
            "signal": rule_result["signal"],
            "method": "RULE",
            "confidence": 1.0,
        }

    nlp_result = classify_with_nlp(description)

    if nlp_result["confidence"] >= NLP_CONFIDENCE_THRESHOLD:
        return {
            "signal": nlp_result["signal"],
            "method": "NLP",
            "confidence": nlp_result["confidence"],
        }

    return {
        "signal": "UNCLASSIFIED",
        "method": "NONE",
        "confidence": nlp_result["confidence"],
    }