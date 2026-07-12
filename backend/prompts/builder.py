from backend.prompts.templates import SYSTEM_PROMPT


def build_prompt(
    query: str,
    context: str,
    conversation: str | None = None,
    conversation_summary: str | None = None,
):
    """
    Build the final RAG prompt.
    """

    return (
        f"{SYSTEM_PROMPT}\n\n"
        f"Conversation Summary:\n"
        f"{conversation_summary or 'No conversation summary.'}\n\n"
        f"Recent Conversation:\n"
        f"{conversation or 'No previous conversation.'}\n\n"
        f"Retrieved Context:\n"
        f"{context}\n\n"
        f"Current Question:\n"
        f"{query}"
    )