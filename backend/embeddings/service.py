from backend.embeddings.model import model
from typing import List
import numpy as np

class EmbeddingService:
    """
    Service responsible for generating text embeddings.
    """

    def embed(self, text:str) -> np.ndarray:
        """
        Generate an embedding for a single piece of text.
        """
        return model.encode(text)

    def embed_documents(self, documents: List[str]) -> np.ndarray:
        """
        Generate embeddings for multiple documents.
        """
        return model.encode(documents)