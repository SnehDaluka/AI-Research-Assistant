class EmbeddingConfig:
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class LLMConfig:
    MODEL = "qwen2.5:3b"
    TEMPERATURE = 0.2


class RetrievalConfig:
    SEARCH_TOP_K = 10
    CONTEXT_TOP_K = 3
    SIMILARITY_THRESHOLD = 0.5
    
class DebugConfig:
    DEBUG = True
    SHOW_SEARCH_RESULTS = True