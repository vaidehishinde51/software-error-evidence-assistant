import json
import sys
from pathlib import Path

# Allow importing backend when script is run from project root
PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from backend.retriever import Retriever


TEST_FILE = (
    PROJECT_ROOT /
    "evaluation" /
    "test_queries.json"
)


def load_test_queries():

    with open(
        TEST_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


def evaluate():

    print("==============================")
    print(" RAG RETRIEVAL EVALUATION")
    print("==============================")

    retriever = Retriever()

    test_queries = load_test_queries()

    correct = 0
    total = len(test_queries)

    print(
        f"\nTesting {total} queries...\n"
    )

    for i, test in enumerate(
        test_queries,
        start=1
    ):

        query = test["query"]

        expected_error = (
            test["expected_error"]
        )

        expected_technology = (
            test["expected_technology"]
        )

        is_unknown_query = (
            expected_error is None
        )

        results = retriever.search(
            query,
            top_k=3
        )

        found = False

        if is_unknown_query:

            # For an unknown query, success means
            # that no evidence passed our threshold.

            if not results:
                found = True

        else:

            for result in results:

                metadata = result["metadata"]

                if (
                 metadata["error_type"]
                 == expected_error
                 and
                 metadata["technology"]
                 == expected_technology
                 ):

                 found = True
                 break

        if found:

            correct += 1

            status = "PASS"

        else:

            status = "FAIL"

        print(
            f"[{status}] {query}"
        )

        if results:

            top = results[0]

            print(
                f"     Retrieved: "
                f"{top['metadata']['error_type']}"
            )

            print(
                f"     Score: "
                f"{top['score']:.4f}"
            )

        else:

            print(
                "     Retrieved: None"
            )

    accuracy = (
        correct / total
    ) * 100

    print("\n==============================")
    print("RESULT")
    print("==============================")

    print(
        f"Correct retrievals: "
        f"{correct}/{total}"
    )

    print(
        f"Retrieval accuracy: "
        f"{accuracy:.2f}%"
    )


if __name__ == "__main__":
    evaluate()