from pathlib import Path

STORAGE_DIR = Path("backend/storage")

STORAGE_DIR.mkdir(parents=True, exist_ok=True)

INDEX_PATH = STORAGE_DIR / "faiss.index"

DOCUMENTS_PATH = STORAGE_DIR / "documents.pkl"