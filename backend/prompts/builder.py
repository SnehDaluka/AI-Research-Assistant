from backend.prompts.templates import SYSTEM_PROMPT


def build_prompt(
    query: str,
    context: str,
):
    """
    Build the final prompt.
    """

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Context:\n"
        f"{context}\n\n"
        f"Question:\n"
        f"{query}"
    )