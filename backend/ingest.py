from pathlib import Path
import json
import re


# -----------------------------
# Configuration
# -----------------------------

RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# -----------------------------
# Text cleaning
# -----------------------------

def clean_text(text: str) -> str:
    """
    Clean unnecessary whitespace from extracted text.
    """
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# -----------------------------
# Chunking
# -----------------------------

def create_chunks(text: str):
    """
    Split text into overlapping chunks.

    Each chunk overlaps with the previous chunk
    so that important information near chunk
    boundaries is not completely lost.
    """

    words = text.split()

    chunks = []

    start = 0
    chunk_id = 0

    while start < len(words):

        end = min(start + CHUNK_SIZE, len(words))

        chunk_words = words[start:end]

        chunk_text = " ".join(chunk_words)

        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })

        chunk_id += 1

        # Move forward while keeping overlap
        start += CHUNK_SIZE - CHUNK_OVERLAP

    return chunks


# -----------------------------
# Process documents
# -----------------------------

def process_document(file_path: Path):

    print(f"\nProcessing: {file_path.name}")

    text = file_path.read_text(
        encoding="utf-8"
    )

    text = clean_text(text)

    chunks = create_chunks(text)

    processed_chunks = []

    for chunk in chunks:

        processed_chunks.append({
            "chunk_id": chunk["chunk_id"],
            "text": chunk["text"],
            "metadata": {
                "source": file_path.name,
                "file_type": file_path.suffix,
                "document_path": str(file_path)
            }
        })

    return processed_chunks


# -----------------------------
# Main
# -----------------------------

def main():

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    all_chunks = []

    files = list(RAW_DATA_DIR.glob("*.txt"))

    if not files:
        print("No documents found in data/raw/")
        return

    for file_path in files:

        chunks = process_document(file_path)

        all_chunks.extend(chunks)

    output_file = (
        PROCESSED_DATA_DIR / "chunks.json"
    )

    with open(
        output_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n-----------------------------")
    print("Document processing complete!")
    print(f"Documents processed: {len(files)}")
    print(f"Total chunks: {len(all_chunks)}")
    print(f"Saved to: {output_file}")
    print("-----------------------------")


if __name__ == "__main__":
    main()