from pathlib import Path
import json

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# --------------------------------
# Configuration
# --------------------------------

CHUNKS_FILE = Path("data/processed/chunks.json")
VECTORSTORE_DIR = Path("vectorstore")

INDEX_FILE = VECTORSTORE_DIR / "faiss.index"
METADATA_FILE = VECTORSTORE_DIR / "metadata.json"

MODEL_NAME = "all-MiniLM-L6-v2"


# --------------------------------
# Load chunks
# --------------------------------

def load_chunks():

    with open(
        CHUNKS_FILE,
        "r",
        encoding="utf-8"
    ) as file:

        return json.load(file)


# --------------------------------
# Create embeddings
# --------------------------------

def create_embeddings(chunks):

    print("Loading embedding model...")

    model = SentenceTransformer(MODEL_NAME)

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    print(f"Creating embeddings for {len(texts)} chunks...")

    embeddings = model.encode(
        texts,
        convert_to_numpy=True,
        show_progress_bar=True
    )

    return embeddings


# --------------------------------
# Create FAISS index
# --------------------------------

def create_faiss_index(embeddings):

    # Convert to float32 because FAISS expects it
    embeddings = embeddings.astype("float32")

    # Normalize vectors
    faiss.normalize_L2(embeddings)

    dimension = embeddings.shape[1]

    print(f"Embedding dimension: {dimension}")

    # Inner Product + normalized vectors
    # behaves like cosine similarity
    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    return index


# --------------------------------
# Save vector store
# --------------------------------

def save_vectorstore(index, chunks):

    VECTORSTORE_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    with open(
        METADATA_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\nVector store created!")
    print(f"FAISS index: {INDEX_FILE}")
    print(f"Metadata: {METADATA_FILE}")


# --------------------------------
# Main
# --------------------------------

def main():

    if not CHUNKS_FILE.exists():

        print(
            "chunks.json not found. "
            "Run ingest.py first."
        )

        return

    chunks = load_chunks()

    if not chunks:

        print("No chunks found.")

        return

    embeddings = create_embeddings(chunks)

    index = create_faiss_index(
        embeddings
    )

    save_vectorstore(
        index,
        chunks
    )

    print("\nEmbedding pipeline completed!")


if __name__ == "__main__":
    main()