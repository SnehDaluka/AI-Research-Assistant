from sentence_transformers import SentenceTransformer

from backend.config import EMBEDDING_MODEL

model = SentenceTransformer(EMBEDDING_MODEL)