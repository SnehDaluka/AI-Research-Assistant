from backend.retrieval.document_store import build_document_store
from backend.retrieval.semantic_search import search
from backend.embeddings.model import model
from backend.prompts.builder import build_prompt


def display_results(results):
    """Display search results in a readable format."""

    print("\nTop Results")
    print("=" * 60)

    if not results:
        print("No relevant documents found.")
        return

    for i, result in enumerate(results, start=1):
        print(f"{i}. {result['text']}")
        print(f"Similarity Score: {result['score']:.4f}")
        print("-" * 60)


def main():
    print("=" * 60)
    print("AI Research Assistant")
    print("=" * 60)

    # Build the document store
    document_store = build_document_store()

    while True:
        query = input("\nAsk a question (or type 'exit'): ").strip()

        if query.lower() == "exit":
            print("\nGoodbye!")
            break

        results = search(query, document_store, model)
        
        prompt = build_prompt(query, results)
        
        # answer = llm.generate(prompt)

        display_results(results)


if __name__ == "__main__":
    main()