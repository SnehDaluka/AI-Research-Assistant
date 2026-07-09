import faiss
import pickle

from typing import List
import numpy as np

from backend.config import RetrievalConfig
from backend.models.document import Document
from backend.models.search_result import SearchResult

from backend.storage.paths import (
    INDEX_PATH,
    DOCUMENTS_PATH,
)


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

    def semantic_search(self, query_embedding: np.ndarray, top_k: int = RetrievalConfig.TOP_K) -> List[SearchResult]:
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
        Clear all documents and recreate the FAISS index.
        """

        self.documents.clear()

        self.index = faiss.IndexFlatIP(
            self.embedding_service.dimension()
        )
        
    def save(self):
        """
        Persist the FAISS index and documents.
        """

        faiss.write_index(
            self.index,
            str(INDEX_PATH),
        )

        with open(DOCUMENTS_PATH, "wb") as file:
            pickle.dump(
                self.documents,
                file,
            )

    def load(self):
        """
        Load the FAISS index and documents.
        """

        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        with open(DOCUMENTS_PATH, "rb") as file:
            self.documents = pickle.load(file)

    def exists(self):
        """
        Return True if a persisted knowledge base exists.
        """

        return (
            INDEX_PATH.exists()
            and DOCUMENTS_PATH.exists()
        )