from backend.models.document import Document


def chunk_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20,
):
    """
    Split text into overlapping chunks.
    """

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive.")

    if overlap < 0:
        raise ValueError("overlap must be non-negative.")

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size.")

    if not text.strip():
        return []

    words = text.split()

    step = chunk_size - overlap

    documents = []

    chunk_id = 0

    for start in range(0, len(words), step):

        chunk = " ".join(
            words[start:start + chunk_size]
        ).strip()

        if not chunk:
            continue

        documents.append(
            Document(
                chunk_id=chunk_id,
                text=chunk
            )
        )

        chunk_id += 1

    return documents