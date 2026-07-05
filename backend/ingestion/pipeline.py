from backend.ingestion.loader import load_pdf
from backend.ingestion.extractor import extract_text
from backend.ingestion.chunker import chunk_text


class IngestionPipeline:
    """
    Coordinates the document ingestion process.
    """

    def __init__(
        self,
        embedding_service,
        document_store,
    ):
        self.embedding_service = embedding_service
        self.document_store = document_store

    def ingest_pdf(self, pdf_path: str):
        """
        Ingest a PDF into the document store.
        """

        pdf = load_pdf(pdf_path)

        text = extract_text(str(pdf))

        documents = chunk_text(text)

        embeddings = self.embedding_service.embed_documents(
            documents
        )

        self.document_store.add_documents(
            documents,
            embeddings
        )

        return len(documents)