class EmbeddingConfig:
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class LLMConfig:
    MODEL = "qwen2.5:3b"
    TEMPERATURE = 0.2


class RetrievalConfig:
    TOP_K = 5
    SIMILARITY_THRESHOLD = 0.4
    
class DebugConfig:
    DEBUG = True
    SHOW_SEARCH_RESULTS = True