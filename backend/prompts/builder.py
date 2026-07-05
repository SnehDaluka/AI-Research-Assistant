from backend.config import RetrievalConfig
from backend.prompts.templates import SYSTEM_PROMPT


def build_prompt(query, search_results):
    """
    Build a prompt for the LLM using retrieved context.
    """

    relevant_results = [
        result
        for result in search_results
        if result.score >= RetrievalConfig.SIMILARITY_THRESHOLD
    ]

    prompt_parts = [
        SYSTEM_PROMPT,
        "",
        "Context:"
    ]

    if relevant_results:

        for index, result in enumerate(relevant_results, start=1):

            prompt_parts.append(
                (
                    f"[Document {index}]\n"
                    f"Source: {result.document.source.filename}\n"
                    f"Page: {result.document.page}\n\n"
                    f"{result.document.text}"
                )
            )

    else:

        prompt_parts.append(
            "No relevant context was found."
        )

    prompt_parts.append(
        (
            "\nInstructions:\n"
            "- Answer only using the provided context.\n"
            "- If the answer is not in the context, clearly say you don't know.\n"
            "- Cite the source document and page number whenever possible."
        )
    )

    prompt_parts.append(f"\nQuestion:\n{query}")

    return "\n\n".join(prompt_parts)