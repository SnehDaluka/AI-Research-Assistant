class EmbeddingConfig:
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"


class LLMConfig:
    MODEL = "qwen2.5:3b"
    TEMPERATURE = 0.2
    
class RerankerConfig:
    MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

class RetrievalConfig:
    SEARCH_TOP_K = 10
    RERANK_TOP_K = 5
    ENABLE_RERANKING = True
    RERANK_SCORE_MARGIN = 0.05
    SIMILARITY_THRESHOLD = 0.5
    ENABLE_QUERY_REWRITING = True
    
class DebugConfig:
    DEBUG = True
    SHOW_SEARCH_RESULTS = True