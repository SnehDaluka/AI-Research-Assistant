from dataclasses import dataclass


@dataclass(slots=True)
class Document:
    text: str
    chunk_id: int