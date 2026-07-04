from backend.embeddings.vector_math import cosine_similarity
from backend.config import TOP_K
from backend.models.search_result import SearchResult
import faiss


class DocumentStore:
    """
    Stores document chunks and their embeddings.
    Responsible for adding, searching, counting,
    and clearing documents.
    """

    def __init__(self):
        self.documents = []
        self.index = faiss.IndexFlatIP(384)

    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to the store.
        """

        if len(documents) != len(embeddings):
            raise ValueError(
                "The number of documents and embeddings must be equal."
            )

        self.documents.extend(documents)
        self.embeddings.extend(embeddings)

    def search(self, query_embedding, top_k=TOP_K):
        """
        Return the top-k most similar documents.
        """

        similarities = []

        for document, embedding in zip(self.documents, self.embeddings):

            score = cosine_similarity(
                query_embedding,
                embedding
            )

            similarities.append(
                SearchResult(
                    text=document,
                    score=float(score)
                )
            )

        similarities.sort(
            key=lambda x: x.score,
            reverse=True
        )

        return similarities[:top_k]

    def count(self):
        """
        Return the number of stored documents.
        """
        return len(self.documents)

    def clear(self):
        """
        Remove all stored documents and embeddings.
        """

        self.documents.clear()
        self.embeddings.clear()