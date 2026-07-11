from backend.conversation.memory import ConversationMemory
from backend.llm.service import LLMService
from backend.llm.client import OllamaClient
from backend.llm.generator import AnswerGenerator
from backend.query.hybrid_rewriter import HybridRewriter
from backend.query.llm_rewriter import LLMRewriter
from backend.query.rule_based import RuleBasedRewriter
from backend.prompts.context_builder import ContextBuilder
from backend.retrieval.retrieval_pipeline import RetrievalPipeline
from backend.reranking.service import RerankingService
from backend.reranking.cross_encoder import CrossEncoderReranker
from backend.retrieval.semantic_search import SemanticSearch
from backend.retrieval.keyword_search import KeywordSearch
# from backend.evaluation.test import embedding_service
from backend.retrieval.hybrid_search import HybridSearch
from backend.config import DebugConfig
from backend.utils.display import print_search_results
from backend.embeddings.service import EmbeddingService
from backend.retrieval.document_store import DocumentStore
from backend.ingestion.pipeline import IngestionPipeline
from backend.prompts.builder import build_prompt
from backend.llm.generator import generate_answer


def startup():

    # --------------------------------
    # Embeddings
    # --------------------------------

    embedding_service = EmbeddingService()

    # --------------------------------
    # Document Store
    # --------------------------------

    document_store = DocumentStore(
        embedding_service
    )

    # --------------------------------
    # Semantic Search
    # --------------------------------

    semantic_search = SemanticSearch(
        embedding_service,
        document_store,
    )

    # --------------------------------
    # Keyword Search
    # --------------------------------

    keyword_search = KeywordSearch(
        document_store
    )

    # --------------------------------
    # Hybrid Search
    # --------------------------------

    hybrid_search = HybridSearch(
        semantic_search,
        keyword_search,
    )

    # --------------------------------
    # Reranking
    # --------------------------------

    reranking_service = RerankingService()

    reranker = CrossEncoderReranker(
        reranking_service
    )

    # --------------------------------
    # LLM
    # --------------------------------

    ollama_client = OllamaClient()

    llm_service = LLMService(
        ollama_client
    )

    answer_generator = AnswerGenerator(
        llm_service
    )

    # --------------------------------
    # Query Rewriting
    # --------------------------------

    rule_rewriter = RuleBasedRewriter()

    llm_rewriter = LLMRewriter(
        llm_service
    )

    query_rewriter = HybridRewriter(
        rule_rewriter,
        llm_rewriter,
    )

    # --------------------------------
    # Retrieval Pipeline
    # --------------------------------

    retrieval_pipeline = RetrievalPipeline(
        hybrid_search,
        reranker,
        query_rewriter,
    )

    # --------------------------------
    # Context Builder
    # --------------------------------

    context_builder = ContextBuilder()

    # --------------------------------
    # Ingestion
    # --------------------------------

    pipeline = IngestionPipeline(
        embedding_service,
        document_store,
        keyword_search,
    )
    
    
    # --------------------------------
    # Conversation Memory
    # --------------------------------
    
    conversation_memory = ConversationMemory(
        max_messages=10
    )

    # --------------------------------
    # Knowledge Base
    # --------------------------------

    if document_store.exists():

        print("Loading Knowledge Base...")

        document_store.load()

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
        answer_generator,
        conversation_memory
    )


def chat_loop(retrieval_pipeline, context_builder, answer_generator, conversation_memory):
    """
    Start the interactive chat.
    """

    while True:

        query = input("\nAsk a question ('exit' to quit): ").strip()

        if query.lower() == "exit":
            print("\nGoodbye!")
            break
        
        # Get history BEFORE adding current question
        history = (
            conversation_memory.get_messages()
        )

        # Retrieve relevant documents
        results = retrieval_pipeline.search(
            query,
            history,
        )
        
        if DebugConfig.DEBUG and DebugConfig.SHOW_SEARCH_RESULTS:
            print_search_results(results)
            
        # Build RAG context
        context = context_builder.build(
            results
        )

        # Build final RAG prompt
        prompt = build_prompt(
            query,
            context,
        )

        if DebugConfig.DEBUG:
            print("\nPrompt")
            print("-" * 60)
            print(prompt)

        # Generate final answer
        answer = answer_generator.generate(
            prompt
        )
        
        # Store completed conversation turn
        conversation_memory.add_user_message(
            query
        )

        conversation_memory.add_assistant_message(
            answer
        )

        print("\nAnswer")
        print("-" * 60)
        print(answer)


def main():

    retrieval_pipeline, context_builder, answer_generator, conversation_memory = startup()

    chat_loop(retrieval_pipeline, context_builder, answer_generator, conversation_memory)


if __name__ == "__main__":
    main()