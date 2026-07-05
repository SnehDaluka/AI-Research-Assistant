class EmbeddingConfig:
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class LLMConfig:
    MODEL = "qwen2.5:3b"
    TEMPERATURE = 0.2


class RetrievalConfig:
    TOP_K = 10
    SIMILARITY_THRESHOLD = 0.4