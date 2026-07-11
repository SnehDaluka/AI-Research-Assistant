from backend.query.base import QueryRewriter


class HybridRewriter(QueryRewriter):
    """
    Combines rule-based expansion with LLM-based rewriting.
    """

    def __init__(
        self,
        rule_rewriter,
        llm_rewriter,
    ):
        self.rule_rewriter = rule_rewriter
        self.llm_rewriter = llm_rewriter

    def rewrite(self, query: str) -> str:

        expanded_query = self.rule_rewriter.rewrite(
            query
        )

        rewritten_query = self.llm_rewriter.rewrite(
            expanded_query
        )

        return rewritten_query