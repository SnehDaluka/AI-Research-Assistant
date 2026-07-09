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
    ):
        self.hybrid_search = hybrid_search
        self.reranker = reranker

    def search(self, query: str):

        results = self.hybrid_search.search(query)

        if not results:
            return []

        if (
            RetrievalConfig.ENABLE_RERANKING
            and self._should_rerank(results)
        ):
            results = self.reranker.rerank(
                query,
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