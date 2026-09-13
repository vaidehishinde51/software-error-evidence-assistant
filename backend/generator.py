import ollama


MODEL_NAME = "llama3.2:latest"


def generate_answer(query, evidence):

    if not evidence:
        return (
            "The available evidence is insufficient "
            "to answer this question reliably."
        )

    context_parts = []

    for i, result in enumerate(evidence, start=1):

        source = result["metadata"]["source"]
        error_type = result["metadata"]["error_type"]
        technology = result["metadata"]["technology"]
        text = result["text"]

        context_parts.append(
            f"""
Evidence {i}
Technology: {technology}
Error Type: {error_type}
Source: {source}

{text}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a software error troubleshooting assistant.

Answer the user's question using ONLY the evidence
provided below.

USER QUESTION:
{query}

RETRIEVED EVIDENCE:
{context}

RULES:

1. Explain the likely cause using the retrieved evidence.
2. Provide practical troubleshooting steps supported
   by the evidence.
3. Do not invent commands, causes, or solutions that
   are not supported by the evidence.
4. If you make an inference, clearly identify it as an
   inference.
5. If the evidence does not provide enough information,
   say that the available evidence is insufficient.
6. Mention the relevant source and error type.
7. Keep the answer concise and useful.

Answer:
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]