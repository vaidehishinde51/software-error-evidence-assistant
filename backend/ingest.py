from pathlib import Path
import json
import re


RAW_DATA_DIR = Path("data/raw")
PROCESSED_DATA_DIR = Path("data/processed")

OUTPUT_FILE = PROCESSED_DATA_DIR / "chunks.json"


TECHNOLOGY_MAP = {
    "python_errors.txt": "Python",
    "java_errors.txt": "Java",
    "javascript_errors.txt": "JavaScript/Node.js",
    "docker_errors.txt": "Docker"
}


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


def create_chunks(text: str, file_path: Path):
    """
    Split the document using blank-line-separated sections.

    Each section contains one error and its supporting
    information.
    """

    sections = re.split(
        r"\n\s*\n",
        text
    )

    chunks = []

    technology = TECHNOLOGY_MAP.get(
        file_path.name,
        "Unknown"
    )

    for section in sections:

        section = section.strip()

        if not section:
            continue

        lines = section.splitlines()

        # Skip document title
        if len(lines) < 2:
            continue

        error_type = lines[0].strip()

        # Ignore the overall document title
        if "TROUBLESHOOTING GUIDE" in error_type.upper():
            continue

        chunks.append({
            "chunk_id": len(chunks),
            "text": section,
            "metadata": {
                "source": file_path.name,
                "file_type": file_path.suffix,
                "document_path": str(file_path),
                "technology": technology,
                "error_type": error_type
            }
        })

    return chunks


def process_document(file_path: Path):

    print(f"\nProcessing: {file_path.name}")

    text = file_path.read_text(
        encoding="utf-8"
    )

    text = clean_text(text)

    chunks = create_chunks(
        text,
        file_path
    )

    print(
        f"Created {len(chunks)} chunks."
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

    # Give every chunk a globally unique ID
    for i, chunk in enumerate(all_chunks):
        chunk["chunk_id"] = i

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