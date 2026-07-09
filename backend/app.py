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

    embedding_service = EmbeddingService()

    document_store = DocumentStore(embedding_service)

    keyword_search = KeywordSearch(document_store)

    pipeline = IngestionPipeline(
        embedding_service,
        document_store,
        keyword_search,
    )

    if document_store.exists():
        print("=" * 60)
        print("Loading Knowledge Base...")
        print("=" * 60)

        document_store.load()

        print(
            f"Loaded {document_store.count()} documents."
        )

    else:

        pipeline.ingest_directory(
            "backend/documents"
        )

        document_store.save()

        print("Knowledge Base saved.")

    return embedding_service, document_store


def chat_loop(
    embedding_service,
    document_store,
):
    """
    Start the interactive chat.
    """
    
    hybrid_search = HybridSearch(
        embedding_service,
        document_store,
    )

    while True:

        query = input("\nAsk a question ('exit' to quit): ").strip()

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        search_results = hybrid_search.search(query)

        if DebugConfig.DEBUG and DebugConfig.SHOW_SEARCH_RESULTS:
            print_search_results(search_results)

        prompt = build_prompt(
            query,
            search_results,
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

    embedding_service, document_store = startup()

    chat_loop(
        embedding_service,
        document_store,
    )


if __name__ == "__main__":
    main()