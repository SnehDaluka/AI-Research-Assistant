# AI Research Assistant

An intelligent, interactive Retrieval-Augmented Generation (RAG) system built in Python and React. This research assistant uses a combination of semantic search, keyword search, and a local LLM to answer complex queries over a local knowledge base.

## Features

- **Hybrid Search Retrieval**: Combines FAISS-based Semantic Search and BM25-based Keyword Search for robust document retrieval.
- **Advanced Query Rewriting**: Uses both Rule-Based and LLM-driven query rewriting to enhance search intent and accuracy.
- **Reranking**: Utilizes a Cross-Encoder (`ms-marco-MiniLM-L-6-v2`) to accurately rerank retrieved documents.
- **Local LLM Integration**: Powered by `qwen2.5:3b` for answering questions, providing local, privacy-first AI responses.
- **Document Ingestion API**: Automatically ingest and index documents via a RESTful API endpoint.
- **Modern Web Interface**: A sleek, dark-mode responsive frontend built with React, Material UI, and Redux Toolkit Query.
- **RESTful API**: Fast and asynchronous API powered by FastAPI.

## Tech Stack

- **Backend**: Python, FastAPI
- **Frontend**: React, Vite, Material UI (MUI), Redux Toolkit (RTK) Query, React Router
- **Embeddings**: `sentence-transformers/all-MiniLM-L6-v2`
- **Reranker**: `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **LLM**: Qwen 2.5 3B (via Ollama)
- **Vector Search**: NumPy / FAISS-based semantic search

## Project Structure

```
├── backend/            # Python API & Core logic
│   ├── api/            # FastAPI application and routers
│   ├── app.py          # Legacy CLI application
│   ├── config.py       # Configuration settings
│   ├── documents/      # Uploaded documents storage
│   ├── embeddings/     # Embedding service and models
│   ├── ingestion/      # Document ingestion pipeline
│   ├── llm/            # LLM client and generator
│   ├── query/          # Query rewriters (Rule-based, LLM, Hybrid)
│   ├── reranking/      # Cross-encoder reranking service
│   └── retrieval/      # Semantic, Keyword, and Hybrid search logic
├── frontend/           # React web application
│   ├── src/            # Source code (Components, API slice, Theme)
│   ├── package.json    # Node dependencies
│   └── vite.config.ts  # Vite configuration
├── docs/               # Documentation
├── data/               # Persistent data / Knowledge base
├── notebooks/          # Jupyter notebooks for experimentation
└── tests/              # Unit tests
```

## Setup & Installation

### 1. Backend Setup

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

### 2. Frontend Setup

1. **Navigate to the frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install node dependencies:**
   ```bash
   npm install
   ```

## Usage

You need to run both the backend API and the frontend development server to use the web interface.

### 1. Start the Backend API
From the root directory, start the FastAPI server:
```bash
uvicorn backend.api.app:app --reload
```
The API will be available at `http://localhost:8000`.

### 2. Start the Frontend
In a new terminal window, navigate to the `frontend` directory and start the Vite development server:
```bash
cd frontend
npm run dev
```
Open the provided URL (usually `http://localhost:5173`) in your browser to access the AI Research Assistant.

## Configuration

You can tweak the backend parameters in `backend/config.py`:
- `RetrievalConfig`: Change `SEARCH_TOP_K`, `RERANK_TOP_K`, and toggle query rewriting.
- `LLMConfig`: Change the target LLM or temperature.