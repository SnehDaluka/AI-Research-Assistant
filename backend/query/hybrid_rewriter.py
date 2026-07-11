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

    def rewrite(self, query: str, history=None) -> str:

        standalone_query = (
            self.llm_rewriter.rewrite(
                query,
                history,
            )
        )

        expanded_query = (
            self.rule_rewriter.rewrite(
                standalone_query
            )
        )

        return expanded_query