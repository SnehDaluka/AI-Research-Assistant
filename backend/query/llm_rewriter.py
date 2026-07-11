from backend.query.base import QueryRewriter


class LLMRewriter(QueryRewriter):
    """
    Uses an LLM to rewrite a query for better retrieval.
    """

    def __init__(self, llm_service):
        self.llm_service = llm_service

    def rewrite(self, query: str) -> str:

        prompt = (
            "Rewrite the following search query to improve "
            "document retrieval.\n\n"
            "Rules:\n"
            "- Keep the original meaning unchanged.\n"
            "- Expand abbreviations when appropriate.\n"
            "- Make the query clear and descriptive.\n"
            "- Do not answer the question.\n"
            "- Return only the rewritten query.\n\n"
            f"Original query:\n{query}"
        )

        rewritten_query = self.llm_service.generate(
            prompt
        )

        return rewritten_query.strip()