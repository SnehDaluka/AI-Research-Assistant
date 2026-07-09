from backend.retrieval.rank_fusion import (
    ReciprocalRankFusion,
)


class HybridSearch:

    def __init__(
        self,
        semantic_search,
        keyword_search,
    ):

        self.semantic_search = semantic_search

        self.keyword_search = keyword_search

        self.rrf = ReciprocalRankFusion()

    def search(
        self,
        query: str,
    ):

        semantic_results = (
            self.semantic_search.search(query)
        )

        keyword_results = (
            self.keyword_search.search(query)
        )

        return self.rrf.fuse(
            semantic_results,
            keyword_results,
        )