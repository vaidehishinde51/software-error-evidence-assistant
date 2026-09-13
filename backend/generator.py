import ollama


MODEL_NAME = "llama3.2:latest"


def generate_answer(query, evidence):

    if not evidence:

        return (
            "The available evidence is insufficient "
            "to answer this question reliably."
        )

    context_parts = []

    for i, result in enumerate(
        evidence,
        start=1
    ):

        context_parts.append(
            f"""
[EVIDENCE {i}]
Source: {result["metadata"]["source"]}
Technology: {result["metadata"]["technology"]}
Error Type: {result["metadata"]["error_type"]}

{result["text"]}
"""
        )

    context = "\n".join(context_parts)

    prompt = f"""
You are a software troubleshooting assistant.

You MUST answer using ONLY the evidence provided below.

USER QUESTION:
{query}

EVIDENCE:
{context}

STRICT RULES:

1. Do not use outside knowledge.
2. Do not invent commands.
3. Do not add troubleshooting steps that are not
   explicitly supported by the evidence.
4. Do not assume that a common solution is applicable.
5. Every factual troubleshooting claim must be
   supported by the evidence.
6. If the evidence does not contain enough information,
   state:

   "The available evidence is insufficient to answer
   this question reliably."

7. Identify the relevant error type.
8. Identify the source used.
9. Keep the answer concise.

ANSWER FORMAT:

Error:
<error type>

Likely cause:
<cause supported by evidence>

Troubleshooting:
<numbered steps supported by evidence>

Evidence source:
<source>

Answer only from the supplied evidence.
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