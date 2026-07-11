from backend.prompts.templates import SYSTEM_PROMPT


def build_prompt(
    query: str,
    context: str,
    conversation: str | None = None,
):
    """
    Build the final RAG prompt.
    """

    if not conversation:
        conversation = "No previous conversation."

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Recent Conversation:\n"
        f"{conversation}\n\n"
        f"Retrieved Context:\n"
        f"{context}\n\n"
        f"Current Question:\n"
        f"{query}"
    )