from sentence_transformers import SentenceTransformer

from backend.config import MODEL_NAME

model = SentenceTransformer(MODEL_NAME)