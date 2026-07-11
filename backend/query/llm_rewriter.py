from backend.query.base import QueryRewriter
from backend.llm.generator import generate_answer


class LLMRewriter(QueryRewriter):
    """
    Uses the local LLM to rewrite the query.
    """

    def rewrite(self, query: str) -> str:

        prompt = f"""
Rewrite the following search query to improve document retrieval.

Rules:
- Keep the meaning unchanged.
- Expand abbreviations when appropriate.
- Return ONLY the rewritten query.
- Do not answer the question.

Query:
{query}
"""

        rewritten = generate_answer(prompt)

        return rewritten.strip()