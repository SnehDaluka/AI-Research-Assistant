from backend.query.base import QueryRewriter


class HybridRewriter(QueryRewriter):
    """
    Combines multiple rewriting strategies.
    """

    def __init__(
        self,
        rule_rewriter,
        llm_rewriter,
    ):
        self.rule_rewriter = rule_rewriter
        self.llm_rewriter = llm_rewriter

    def rewrite(self, query: str) -> str:

        query = self.rule_rewriter.rewrite(query)

        query = self.llm_rewriter.rewrite(query)

        return query