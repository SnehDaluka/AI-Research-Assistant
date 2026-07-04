from backend.embeddings.vector_math import cosine_similarity
from backend.config import TOP_K
from backend.models.search_result import SearchResult
from backend.embeddings.service import EmbeddingService
import faiss


class DocumentStore:
    """
    Stores document chunks and their embeddings.
    Responsible for adding, searching, counting,
    and clearing documents.
    """

    def __init__(self):
        self.documents = []
        embedding_service = EmbeddingService()
        dimension = embedding_service.dimension()
        self.index = faiss.IndexFlatIP(dimension)

    def add_documents(self, documents, embeddings):
        """
        Add documents and their embeddings to the store.
        """

        if len(documents) != len(embeddings):
            raise ValueError(
                "The number of documents and embeddings must be equal."
            )

        self.documents.extend(documents)
        self.index.add(embeddings)

    def search(self, query_embedding, top_k=TOP_K):
        """
        Return the top-k most similar documents.
        """

        similarities = []
        
        distances, indices = self.index.search(query_embedding, top_k)

        for idx, distance in zip(indices[0], distances[0]):
            similarities.append(
                SearchResult(
                    text=self.documents[idx],
                    score=float(distance)
                )
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