from backend.retrieval.document_store import build_document_store
from backend.retrieval.semantic_search import search
from backend.prompts.builder import build_prompt
from backend.llm.generator import generate_answer


def main():
    print("=" * 60)
    print("AI Research Assistant")
    print("=" * 60)

    document_store = build_document_store()

    while True:
        query = input("\nAsk a question (type 'exit' to quit): ").strip()

        if query.lower() == "exit":
            break

        search_results = search(query, document_store)

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