from backend.config import RetrievalConfig
from backend.models.document import Document
from backend.models.search_result import SearchResult
import faiss
from typing import List
import numpy as np


class DocumentStore:
    """
    Stores document chunks and their embeddings.
    Responsible for adding, searching, counting,
    and clearing documents.
    """

    def __init__(self, embedding_service):
        self.documents = []
        self.embedding_service = embedding_service
        self.index = faiss.IndexFlatIP(self.embedding_service.dimension())

    def add_documents(self, documents: List[Document], embeddings: np.ndarray) -> None:
        """
        Add documents and their embeddings to the store.
        """

        if len(documents) != len(embeddings):
            raise ValueError(
                "The number of documents and embeddings must be equal."
            )

        self.documents.extend(documents)
        
        if embeddings.ndim != 2:
            raise ValueError("Embeddings must be a 2D NumPy array.")

        self.index.add(embeddings)

    def search(self, query_embedding: np.ndarray, top_k: int = RetrievalConfig.TOP_K) -> List[SearchResult]:
        """
        Return the top-k most similar documents.
        """
        
        if query_embedding.ndim != 2:
            raise ValueError("Query embedding must have shape (1, dimension).")

        results = []
        
        if self.count() == 0:
            return []
        
        distances, indices = self.index.search(query_embedding, top_k)

        for document_index, score in zip(indices[0], distances[0]):
            if document_index == -1:
                continue
            
            results.append(
                SearchResult(
                    document=self.documents[document_index],
                    score=float(score)
                )
            )
        
        return results

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
        self.index = faiss.IndexFlatIP(self.embedding_service.dimension())