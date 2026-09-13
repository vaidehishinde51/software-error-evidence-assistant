from pathlib import Path
import json
import re


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

OUTPUT_FILE = PROCESSED_DATA_DIR / "chunks.json"


def clean_text(text: str) -> str:
    """Clean unnecessary whitespace."""

    text = text.replace("\r\n", "\n")

    text = re.sub(
        r"[ \t]+",
        " ",
        text
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text
    )

    return text.strip()


def create_error_chunks(text: str, file_path: Path):
    """
    Create one chunk for each documented error.

    The document uses error names as section headings.
    """

    # Find sections beginning with known error names
    pattern = r"(?m)^(ModuleNotFoundError|NameError|TypeError|IndexError|KeyError)\s*$"

    matches = list(re.finditer(pattern, text))

    chunks = []

    for i, match in enumerate(matches):

        start = match.start()

        if i + 1 < len(matches):
            end = matches[i + 1].start()
        else:
            end = len(text)

        section = text[start:end].strip()

        error_name = match.group(1)

        chunks.append({
            "chunk_id": len(chunks),
            "text": section,
            "metadata": {
                "source": file_path.name,
                "file_type": file_path.suffix,
                "document_path": str(file_path),
                "technology": "Python",
                "error_type": error_name
            }
        })

    return chunks


def process_document(file_path: Path):

    print(f"\nProcessing: {file_path.name}")

    text = file_path.read_text(
        encoding="utf-8"
    )

    text = clean_text(text)

    chunks = create_error_chunks(
        text,
        file_path
    )

    print(
        f"Created {len(chunks)} meaningful chunks."
    )

    return chunks


def main():

    PROCESSED_DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    all_chunks = []

    files = list(
        RAW_DATA_DIR.glob("*.txt")
    )

    if not files:

        print(
            "No .txt documents found in data/raw/"
        )

        return

    for file_path in files:

        chunks = process_document(
            file_path
        )

        all_chunks.extend(chunks)

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_chunks,
            file,
            indent=2,
            ensure_ascii=False
        )

    print("\n==============================")
    print("INGESTION COMPLETE")
    print("==============================")
    print(
        f"Documents processed: {len(files)}"
    )
    print(
        f"Total chunks: {len(all_chunks)}"
    )
    print(
        f"Saved to: {OUTPUT_FILE}"
    )


if __name__ == "__main__":
    main()