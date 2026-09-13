from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


INDEX_FILE = Path("vectorstore/faiss.index")
METADATA_FILE = Path("vectorstore/metadata.json")

MODEL_NAME = "all-MiniLM-L6-v2"

# Minimum similarity required for evidence
SIMILARITY_THRESHOLD = 0.45


class Retriever:

    def __init__(self):

        print("Loading vector store...")

        self.index = faiss.read_index(
            str(INDEX_FILE)
        )

        with open(
            METADATA_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            self.metadata = json.load(file)

        print(
            f"Loaded {self.index.ntotal} vectors."
        )

        print("Loading embedding model...")

        self.model = SentenceTransformer(
            MODEL_NAME
        )


    def search(self, query, top_k=3):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        query_embedding = query_embedding.astype(
            "float32"
        )

        faiss.normalize_L2(
            query_embedding
        )

        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            if index == -1:
                continue

            score = float(score)

            # Ignore weak matches
            if score < SIMILARITY_THRESHOLD:
                continue

            chunk = self.metadata[index]

            results.append({
                "score": score,
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            })

        return results


def main():

    retriever = Retriever()

    query = input(
        "\nEnter your error/question: "
    )

    results = retriever.search(
        query,
        top_k=3
    )

    print("\n==============================")
    print("RETRIEVED EVIDENCE")
    print("==============================")

    if not results:

        print(
            "No sufficiently relevant evidence found."
        )

        return

    for i, result in enumerate(
        results,
        start=1
    ):

        print(
            f"\nResult {i}"
        )

        print(
            f"Similarity Score: "
            f"{result['score']:.4f}"
        )

        print(
            f"Technology: "
            f"{result['metadata']['technology']}"
        )

        print(
            f"Error Type: "
            f"{result['metadata']['error_type']}"
        )

        print(
            f"Source: "
            f"{result['metadata']['source']}"
        )

        print("\nText:")
        print(result["text"])


if __name__ == "__main__":
    main()