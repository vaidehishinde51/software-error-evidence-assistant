from pathlib import Path
import json

import faiss
from sentence_transformers import SentenceTransformer


# --------------------------------
# Configuration
# --------------------------------

INDEX_FILE = Path("vectorstore/faiss.index")
METADATA_FILE = Path("vectorstore/metadata.json")

MODEL_NAME = "all-MiniLM-L6-v2"


# --------------------------------
# Retriever
# --------------------------------

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


    # --------------------------------
    # Search
    # --------------------------------

    def search(self, query, top_k=3):

        # Convert query into embedding
        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        )

        # FAISS expects float32
        query_embedding = query_embedding.astype(
            "float32"
        )

        # Normalize for cosine similarity
        faiss.normalize_L2(
            query_embedding
        )

        # Search FAISS
        scores, indices = self.index.search(
            query_embedding,
            top_k
        )

        results = []

        for score, index in zip(
            scores[0],
            indices[0]
        ):

            # -1 means no result
            if index == -1:
                continue

            chunk = self.metadata[index]

            results.append({
                "score": float(score),
                "text": chunk["text"],
                "metadata": chunk["metadata"]
            })

        return results


# --------------------------------
# Test retriever
# --------------------------------

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
            f"Source: "
            f"{result['metadata']['source']}"
        )

        print(
            "\nText:"
        )

        print(
            result["text"]
        )


if __name__ == "__main__":
    main()