from backend.config import RetrievalConfig


def build_prompt(query, search_results):
    """
    Build the user prompt using the retrieved context.
    """

    relevant_results = [
        result
        for result in search_results
        if result["score"] >= RetrievalConfig.SIMILARITY_THRESHOLD
    ]

    if not relevant_results:
        return None

    prompt_parts = [
        "Context:"
    ]

    for index, result in enumerate(relevant_results, start=1):
        prompt_parts.append(
            f"[{index}]\n{result['text']}"
        )

    prompt_parts.append(f"Question:\n{query}")

    return "\n\n".join(prompt_parts)