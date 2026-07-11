from backend.config import RetrievalConfig


class RetrievalPipeline:
    """
    Complete retrieval pipeline.

    Query
      ↓
    Hybrid Search
      ↓
    Optional Cross Encoder
      ↓
    Final Results
    """

    def __init__(
        self,
        hybrid_search,
        reranker,
        query_rewriter,
    ):
        self.hybrid_search = hybrid_search
        self.reranker = reranker
        self.query_rewriter = query_rewriter

    def search(self, query: str):

        rewritten_query = query
        
        if RetrievalConfig.ENABLE_QUERY_REWRITING:
            rewritten_query = self.query_rewriter.rewrite(query)
            
            print("\nQuery Rewritten")
            print("--------------------")
            print(f"Original : {query}")
            print(f"Expanded : {rewritten_query}")

        results = self.hybrid_search.search(rewritten_query)

        if not results:
            return []

        if (
            RetrievalConfig.ENABLE_RERANKING
            and self._should_rerank(results)
        ):
            results = self.reranker.rerank(
                rewritten_query,
                results,
            )

        else:
            results = results[
                : RetrievalConfig.RERANK_TOP_K
            ]

        return results

    def _should_rerank(self, results):

        if len(results) < 2:
            return False

        top_score = results[0].score
        second_score = results[1].score

        difference = top_score - second_score

        return (
            difference <
            RetrievalConfig.RERANK_SCORE_MARGIN
        )