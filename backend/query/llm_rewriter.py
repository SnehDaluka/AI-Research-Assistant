from backend.query.base import QueryRewriter


class LLMRewriter(QueryRewriter):
    """
    Uses an LLM to rewrite a query for better retrieval.
    """

    def __init__(self, llm_service):
        self.llm_service = llm_service

    def rewrite(
        self,
        query: str,
        history=None,
    ) -> str:

        history_text = self._format_history(
            history
        )

        prompt = (
            "Rewrite the user's current question into a "
            "standalone search query for document retrieval.\n\n"
            "Rules:\n"
            "- Use conversation history only when needed.\n"
            "- Resolve pronouns such as 'it', 'this', and 'that'.\n"
            "- Preserve the user's original meaning.\n"
            "- Do not answer the question.\n"
            "- Return only the rewritten query.\n\n"
            f"Conversation History:\n"
            f"{history_text}\n\n"
            f"Current Question:\n"
            f"{query}"
        )

        rewritten_query = self.llm_service.generate(
            prompt
        )

        return rewritten_query.strip()
    
    def _format_history(
        self,
        history,
    ) -> str:

        if not history:
            return "No previous conversation."

        lines = []

        for message in history:

            lines.append(
                f"{message.role.capitalize()}: "
                f"{message.content}"
            )

        return "\n".join(lines)