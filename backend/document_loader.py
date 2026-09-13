from pathlib import Path
import pymupdf


def load_txt(file_path: Path) -> str:

    return file_path.read_text(
        encoding="utf-8"
    )


def load_md(file_path: Path) -> str:

    return file_path.read_text(
        encoding="utf-8"
    )


def load_pdf(file_path: Path) -> str:

    document = pymupdf.open(
        file_path
    )

    pages = []

    for page in document:

        pages.append(
            page.get_text()
        )

    document.close()

    return "\n\n".join(pages)


def load_document(file_path: Path) -> str:

    extension = file_path.suffix.lower()

    if extension == ".txt":

        return load_txt(file_path)

    if extension == ".md":

        return load_md(file_path)

    if extension == ".pdf":

        return load_pdf(file_path)

    raise ValueError(
        f"Unsupported file type: {extension}"
    )