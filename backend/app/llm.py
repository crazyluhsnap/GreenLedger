import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

SYSTEM_PROMPT = """
You are GreenLedger, an ESG intelligence assistant.

Answer questions using only the ESG evidence provided in the context.

Rules:
1. Do not invent financial, transaction, or ESG facts.
2. Do not calculate new ESG scores unless the calculation is explicitly
   supported by the provided evidence.
3. If the context does not contain enough information, say so clearly.
4. Don't be too concise and directly answer the user's question.
5. Avoid repeating the same transaction, signal, anomaly, or recommendation
   multiple times.
6. Prefer short sections and bullet points over long paragraphs.
7. Use a table only when it genuinely makes a comparison clearer.
8. When discussing a transaction, mention its transaction ID when available.
9. When discussing a risk or opportunity, briefly explain why it matters
   using the retrieved evidence.
10. Do not restate the entire evidence context in your answer.
11. Do not add a separate summary that repeats points already explained.
12. Treat GreenLedger's ESG scores, classifications, anomaly detection,
    and recommendations as prototype analytics, not regulatory or
    professional ESG ratings.
13. Keep responses suitable for a professional financial analytics dashboard.
14. Do not claim that a signal is the "only", "biggest", "most important",
    or "highest" signal unless the provided evidence explicitly establishes
    that comparison. Retrieved evidence may be incomplete.
15. If the question asks about the company's overall ESG signals or risks,
    clearly state that the answer is based on the retrieved evidence.
16.Use Markdown only. NEVER output HTML tags such as <br>, <p>, <div>,
   <table>, <ul>, or <li>.
"""


def generate_answer(
    question: str,
    context: str,
) -> str:
    if not question.strip():
        return "Please provide a question."

    if not context.strip():
        return (
            "I don't have enough ESG evidence to answer that question."
        )

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "GROQ_API_KEY is not configured."
        )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": (
                    f"ESG Evidence:\n\n"
                    f"{context}\n\n"
                    f"Question:\n{question}"
                ),
            },
        ],
        temperature=0.2,
        max_tokens=500,
    )

    return response.choices[0].message.content.strip()