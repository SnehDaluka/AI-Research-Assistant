from backend.data.documents import documents
from backend.embeddings.model import model


def build_document_store():
    embeddings = model.encode(documents)

    document_store = []

    for document, embedding in zip(documents, embeddings):
        document_store.append(
            {
                "text": document,
                "embedding": embedding
            }
        )

    return document_store