from dataclasses import dataclass
from backend.models.document import Document


@dataclass
class SearchResult:
    document: Document
    score: float