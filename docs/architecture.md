# AI Research Assistant Architecture

This document describes the production-ready Retrieval-Augmented Generation (RAG) architecture of the AI Research Assistant.

## 1. System Overview

The AI Research Assistant is designed to process PDF documents, extract their knowledge into a semantic search index, and accurately answer user queries based on that knowledge.

Unlike a basic script, this application is built with **Domain-Driven Design (DDD)** and separation of concerns, ensuring scalability, maintainability, and accurate retrieval. It operates in two main phases:
1. **Knowledge Base Creation (Ingestion Mode)**: Processes documents and persists their embeddings and metadata.
2. **Interactive Chat (Retrieval Mode)**: Loads the persisted knowledge base for instantaneous startup and conversational query answering.

---

## 2. Core Domain Models

Instead of passing primitive data types, the system models real-world concepts as Python `dataclasses`.

- **`SourceDocument`**: Represents the original file (e.g., PDF filename and path).
- **`Page`**: Represents a single extracted page from a document, preserving structural boundaries.
- **`Document`**: The core unit of retrieval. It represents a semantic chunk of text and includes metadata:
  - `chunk_id` (Unique identifier)
  - `source` (`SourceDocument`)
  - `page` (Page number)
  - `text` (The actual chunk content)
- **`SearchResult`**: Represents a matched `Document` alongside its cosine similarity `score`.
- **`IngestionResult`**: Represents the outcome of processing a document (e.g., number of chunks created).

By passing these objects throughout the pipeline, the system maintains critical metadata (like source citations and page numbers) from ingestion to the final LLM prompt.

---

## 3. The Ingestion Pipeline

The ingestion pipeline prepares documents for retrieval. It is coordinated by the `IngestionPipeline` class to ensure all components run sequentially.

```text
PDF -> Extractor -> Pages -> Chunker -> Documents -> Embedding Service -> Document Store
```

### Components:
- **Loader**: Validates the PDF file path and existence.
- **Extractor (`PyMuPDF/fitz`)**: Reads the PDF and returns a list of `Page` objects, preserving page boundaries.
- **Chunker**: Splits the pages into smaller, overlapping chunks to fit LLM context windows while preserving meaning. It yields `Document` objects with rich metadata.
- **Embedding Service**: Converts the chunk text into 384-dimensional dense vectors using `sentence-transformers/all-MiniLM-L6-v2`. Embeddings are normalized for optimal cosine similarity search.
- **Document Store**: Stores the vectors in a **FAISS (`IndexFlatIP`)** index and the `Document` objects (metadata) via `pickle`.

### Persistence
Embeddings are computationally expensive to generate. Therefore, the application persists the FAISS index (`faiss.index`) and document metadata (`documents.pkl`) to disk in the `backend/storage` directory. This allows the assistant to skip ingestion on future startups, loading the knowledge base instantly.

---

## 4. The Retrieval Pipeline (Chat Mode)

Once the knowledge base is built and loaded, the application enters the interactive chat loop.

```text
User Query -> Query Embedding -> FAISS Search -> Top-K Filtering -> Prompt Builder -> LLM Generator -> Answer
```

### Components:
- **Semantic Search**: The user's query is embedded and searched against the FAISS index using Cosine Similarity (Inner Product on normalized vectors).
- **Filtering (`DocumentStore.search`)**: Retrieves the `Top K` (e.g., 5) closest chunks, filtering out those below the `SIMILARITY_THRESHOLD`. Returns a list of `SearchResult` objects.
- **Prompt Builder**: Constructs the LLM prompt. It injects the retrieved text alongside its metadata (Source and Page) to enable the LLM to generate citations. It includes strict system instructions to prevent hallucination.
- **LLM Generator (`Ollama`)**: Submits the prompt to a locally hosted LLM (e.g., `qwen2.5:3b`) for private, offline, and cost-free natural language generation.

---

## 5. Directory Structure

```text
backend/
├── app.py                # Main application lifecycle (startup & chat_loop)
├── config.py             # Configuration (Top-K, thresholds, models, debug mode)
├── documents/            # Source PDF files to be ingested
├── embeddings/           # Embedding generation and normalization
├── ingestion/            # Loading, extraction, chunking, and pipeline coordination
├── llm/                  # Local LLM client and generator
├── models/               # Domain models (Document, Page, SearchResult, etc.)
├── prompts/              # Prompt templates and builder logic
├── retrieval/            # FAISS DocumentStore and search logic
├── storage/              # Persisted knowledge base (FAISS index & pickled metadata)
└── utils/                # Debugging and display utilities
```

---

## 6. Debugging and Observability

Retrieval quality dictates answer quality. To facilitate debugging without cluttering the user interface, the system implements a **Developer Mode** (`DebugConfig.DEBUG`).

When enabled, the system uses `utils/display.py` to print:
- Retrieved document ranks and exact similarity scores.
- The metadata (source, page) and text of the chunks sent to the LLM.
- The final constructed prompt.

This visibility makes it easy to diagnose whether an incorrect answer stems from poor chunking, a strict similarity threshold, or LLM hallucination.
