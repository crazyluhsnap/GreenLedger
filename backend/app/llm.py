import os

from groq import Groq


SYSTEM_PROMPT = """
You are GreenLedger, an ESG intelligence assistant.

Answer questions using only the ESG evidence provided in the context.

Rules:
1. Do not invent financial or ESG facts.
2. Do not calculate new ESG scores unless the calculation is explicitly
   supported by the provided evidence.
3. If the context does not contain enough information, say so clearly.
4. Explain your answer in a concise and understandable way.
5. When possible, mention the relevant transaction, period, score,
   signal, anomaly, or recommendation from the evidence.
6. Treat GreenLedger's ESG scores and rules as prototype analytics,
   not regulatory or professional ESG ratings.
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
        model="llama-3.3-70b-versatile",
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