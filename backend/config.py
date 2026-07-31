class EmbeddingConfig:
    MODEL = "sentence-transformers/all-MiniLM-L6-v2"

class ChunkerConfig:
    CHUNK_SIZE = 400
    OVERLAP = 75

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
    SIMILARITY_THRESHOLD = 0.4
    ENABLE_QUERY_REWRITING = True
    
class ConversationConfig:
    MAX_RECENT_TURNS = 5
    SUMMARIZE_TURN_COUNT = 2
    REWRITE_HISTORY_TURNS = 3
    GENERATION_HISTORY_TURNS = 3

class DebugConfig:
    DEBUG = False
    SHOW_SEARCH_RESULTS = False
    
class ObservabilityConfig:
    ENABLE_TRACING = True