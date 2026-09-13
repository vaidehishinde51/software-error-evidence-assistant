from .retriever import Retriever
from .generator import generate_answer


def main():

    print("==============================")
    print(" SOFTWARE ERROR EVIDENCE ASSISTANT")
    print("==============================")

    retriever = Retriever()

    query = input(
        "\nDescribe your software error:\n> "
    )

    print("\nSearching knowledge base...")

    evidence = retriever.search(
        query,
        top_k=3
    )

    if not evidence:

        print(
            "\nNo relevant evidence found."
        )

        return

    print(
        f"Retrieved {len(evidence)} evidence chunks."
    )

    print("\nGenerating grounded answer...")

    answer = generate_answer(
        query,
        evidence
    )

    print("\n==============================")
    print("ANSWER")
    print("==============================")

    print(answer)

    print("\n==============================")
    print("EVIDENCE USED")
    print("==============================")

    for i, result in enumerate(
        evidence,
        start=1
    ):

        print(
            f"\n[{i}] "
            f"{result['metadata']['error_type']}"
        )

        print(
            f"Technology: "
            f"{result['metadata']['technology']}"
        )

        print(
            f"Source: "
            f"{result['metadata']['source']}"
        )

        print(
            f"Similarity: "
            f"{result['score']:.4f}"
        )

        print(
            f"Confidence: "
            f"{result['confidence']}"
        )


if __name__ == "__main__":
    main()