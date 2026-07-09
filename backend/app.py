from backend.prompts.context_builder import ContextBuilder
from backend.retrieval.retrieval_pipeline import RetrievalPipeline
from backend.reranking.service import RerankingService
from backend.reranking.cross_encoder import CrossEncoderReranker
from backend.retrieval.semantic_search import SemanticSearch
from backend.retrieval.keyword_search import KeywordSearch
from backend.evaluation.test import embedding_service
from backend.retrieval.hybrid_search import HybridSearch
from backend.retrieval import hybrid_search
from backend.config import DebugConfig
from backend.utils.display import print_search_results
from backend.embeddings.service import EmbeddingService
from backend.retrieval.document_store import DocumentStore
from backend.ingestion.pipeline import IngestionPipeline
from backend.prompts.builder import build_prompt
from backend.llm.generator import generate_answer


def startup():
    """
    Initialize the application.
    """

    # Core Services
    embedding_service = EmbeddingService()
    document_store = DocumentStore(embedding_service)

    # Search Components
    semantic_search = SemanticSearch(
        embedding_service,
        document_store,
    )

    keyword_search = KeywordSearch(
        document_store,
    )

    hybrid_search = HybridSearch(
        semantic_search,
        keyword_search,
    )

    # Reranker
    reranking_service = RerankingService()

    reranker = CrossEncoderReranker(
        reranking_service,
    )

    # Ingestion Pipeline
    pipeline = IngestionPipeline(
        embedding_service,
        document_store,
        keyword_search,
    )
    
    # Retrieval Pipeline
    retrieval_pipeline = RetrievalPipeline(
        hybrid_search,
        reranker,
    )
    
    # Context Builder
    context_builder = ContextBuilder()

    # Load existing knowledge base or build a new one
    if document_store.exists():

        print("=" * 60)
        print("Loading Knowledge Base...")
        print("=" * 60)

        document_store.load()

        # Rebuild BM25 using the loaded documents
        keyword_search.build_index()

        print(
            f"Loaded {document_store.count()} documents."
        )

    else:

        pipeline.ingest_directory(
            "backend/documents"
        )

        document_store.save()

        print("Knowledge Base saved.")

    return (
        retrieval_pipeline,
        context_builder,
    )


def chat_loop(retrieval_pipeline, context_builder):
    """
    Start the interactive chat.
    """

    while True:

        query = input("\nAsk a question ('exit' to quit): ").strip()

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        results = retrieval_pipeline.search(query)
        
        if DebugConfig.DEBUG and DebugConfig.SHOW_SEARCH_RESULTS:
            print_search_results(results)
            
        context = context_builder.build(results)

        prompt = build_prompt(
            query,
            context,
        )

        if DebugConfig.DEBUG:
            print("\nPrompt")
            print("-" * 60)
            print(prompt)

        answer = generate_answer(prompt)

        print("\nAnswer")
        print("-" * 60)
        print(answer)


def main():

    retrieval_pipeline, context_builder = startup()

    chat_loop(retrieval_pipeline, context_builder)


if __name__ == "__main__":
    main()