# AI Research Assistant

An intelligent, interactive Retrieval-Augmented Generation (RAG) system built in Python. This research assistant uses a combination of semantic search, keyword search, and an LLM to answer complex queries over a local knowledge base.

## Features

- **Hybrid Search Retrieval**: Combines FAISS-based Semantic Search and BM25-based Keyword Search for robust document retrieval.
- **Advanced Query Rewriting**: Uses both Rule-Based and LLM-driven query rewriting to enhance search intent and accuracy.
- **Reranking**: Utilizes a Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) to accurately rerank retrieved documents.
- **Local LLM Integration**: Powered by `qwen2.5:3b` for answering questions, providing local, privacy-first AI responses.
- **Document Ingestion Pipeline**: Automatically ingests and indexes documents from a local directory.
- **Interactive CLI**: Simple command-line chat interface to interact with your knowledge base.

## Tech Stack

- **Language**: Python
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **LLM**: Qwen 2.5 3B
- **Vector Search**: NumPy / FAISS-based semantic search

## Project Structure

```
├── backend/            # Core backend logic
│   ├── app.py          # Main application and chat loop
│   ├── config.py       # Configuration settings
│   ├── documents/      # Directory for documents to ingest
│   ├── embeddings/     # Embedding service and models
│   ├── ingestion/      # Document ingestion pipeline
│   ├── llm/            # LLM client and generator
│   ├── query/          # Query rewriters (Rule-based, LLM, Hybrid)
│   ├── reranking/      # Cross-encoder reranking service
│   └── retrieval/      # Semantic, Keyword, and Hybrid search logic
├── docs/               # Documentation
├── data/               # Persistent data / Knowledge base
├── notebooks/          # Jupyter notebooks for experimentation
└── tests/              # Unit tests
```

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd "AI Research Assistant"
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows
   .venv\Scripts\activate
   # On Linux/macOS
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare Documents:**
   Place any text documents or PDFs you want the assistant to learn from into the `backend/documents/` directory.

## Usage

Start the AI Research Assistant by running the main application script:

```bash
python -m backend.app
# or
python backend/app.py
```

On the first run, the system will ingest the documents in `backend/documents/` and build the search indices. After loading the knowledge base, you will enter the interactive chat loop:

```text
============================================================
Loading Knowledge Base...
============================================================
Loaded X documents.

Ask a question ('exit' to quit): What is this document about?
```

## Configuration

You can tweak the parameters in `backend/config.py`:
- `RetrievalConfig`: Change `SEARCH_TOP_K`, `RERANK_TOP_K`, and toggle query rewriting.
- `LLMConfig`: Change the target LLM or temperature.
- `DebugConfig`: Enable or disable debug logs during the chat loop.