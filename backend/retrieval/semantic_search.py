from backend.embeddings.vector_math import cosine_similarity
from backend.embeddings.model import model


def search(query: str, document_store: list, top_k: int = 3):
    """
    Perform semantic search and return the top_k most similar documents.
    """

    # Generate embedding for the query
    query_embedding = model.encode(query)

    search_results = []

    # Compare query with every document
    for document in document_store:
        score = cosine_similarity(
            query_embedding,
            document["embedding"]
        )

        search_results.append(
            {
                "text": document["text"],
                "score": score
            }
        )

    # Sort by similarity (highest first)
    search_results.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return search_results[:top_k]
