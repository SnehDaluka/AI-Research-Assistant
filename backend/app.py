from backend.embeddings.service import EmbeddingService
from backend.retrieval.document_store import DocumentStore
from backend.prompts.builder import build_prompt
from backend.llm.generator import generate_answer
from pathlib import Path
from backend.ingestion.pipeline import IngestionPipeline


def main():
    print("=" * 60)
    print("AI Research Assistant")
    print("=" * 60)
    
    BASE_DIR = Path(__file__).resolve().parent
    pdf_file = BASE_DIR / "data" / "sample.pdf"
    
    embedding_service = EmbeddingService()
    
    document_store = DocumentStore(embedding_service)

    pipeline = IngestionPipeline(embedding_service, document_store)
    
    pipeline.ingest_pdf(str(pdf_file))

    while True:
        query = input("\nAsk a question (type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            break

        query_embedding = embedding_service.embed_query(query)

        search_results = document_store.search(query_embedding)

        prompt = build_prompt(query, search_results)
        
        print("\nPrompt")
        print("-" * 60)
        print(prompt)

        answer = generate_answer(prompt)

        print("\nAnswer")
        print("-" * 60)
        print(answer)


if __name__ == "__main__":
    main()